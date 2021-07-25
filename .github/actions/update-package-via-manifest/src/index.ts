import * as core from "@actions/core"
import * as github from "@actions/github"
import { promise as glob } from "glob-promise"
import * as fs from "fs"
import * as path from "path"
import { execSync } from "child_process"

try {
	const context = github.context

	// Identify all packages in the pkgs directory
	const manifests = await glob("pkgs/**/.aurmanifest.json")

	for (const manifestPath of manifests) {
		const pkgbuildPath = path.join(manifestPath.replace("/.aurmanifest.json", ""), "PKGBUILD")

		core.info(manifestPath)

		const manifest = JSON.parse(fs.readFileSync(manifestPath).toString()) as IManifest

		const pkgbuildVersion: string | undefined = getVersionFromPKGBUILD(manifestPath.replace("/.aurmanifest.json", ""))
		if (pkgbuildVersion === undefined) {
			core.warning(`Unable to get package version from PKGBUILD (${manifest.name})`)
			continue
		}

		let latestVersion = ""
		switch (manifest.automaticUpdates.type) {
			case "github":
				const ghVersion = await getLatestVersionFromGithub(manifest.automaticUpdates.repo)
				if (ghVersion === undefined) {
					core.warning(`Failed to get latest version from GitHub (${manifestPath}).`)
					continue
				}
				latestVersion = ghVersion.replace(/^v/m, "") // Remove leading v idiom
				break
			default:
				core.warning(`Unknown automaticUpdates type '${manifest.automaticUpdates}' in ${manifestPath}`)
				continue
		}

		core.info(`PKGBUILD: '${pkgbuildVersion}' Latest: '${latestVersion}'`)
		if (pkgbuildVersion === latestVersion) {
			continue
		}

		// Change permissions so that everything "should be" writable
		execSync("sudo chown -R builder:builder $(pwd)", {stdio: 'inherit'})

		// Create new branch
		const branchName = `bot/${manifest.name}/${latestVersion}`
		execSync(`git checkout -b ${branchName}`, {stdio: 'inherit'})

		let pkgbuildContents: string = fs.readFileSync(pkgbuildPath).toString()

		// Update PKGBUILD with new version (pkgver to latestVersion and pkgrel to 1)
		pkgbuildContents = pkgbuildContents.replace(/^pkgver=.*/m, `pkgver=${latestVersion}`)
		pkgbuildContents = pkgbuildContents.replace(/^pkgrel=.*/m, "pkgrel=1")

		fs.writeFileSync(pkgbuildPath, pkgbuildContents)

		// Update checksums in PKGBUILD
		execSync(`updpkgsums`, {
			stdio: "inherit",
			cwd: manifestPath.replace("/.aurmanifest.json", ""),
		})

		// git add and commit updated PKGBUILD
		execSync(`git add ${pkgbuildPath}`, {stdio: 'inherit'})
		execSync(`git commit -m "Update ${manifest.name} to ${latestVersion}"`, {
			stdio: "inherit",
			env: {
				GIT_AUTHOR_NAME: "github-actions[bot]",
				GIT_AUTHOR_EMAIL: "41898282+github-actions[bot]@users.noreply.github.com",
				GIT_COMMITTER_NAME: "github-actions[bot]",
				GIT_COMMITTER_EMAIL: "41898282+github-actions[bot]@users.noreply.github.com",
				EMAIL: "41898282+github-actions[bot]@users.noreply.github.com",
			}
		})

		// Push changes to GitHub
		execSync(`git push origin ${branchName}`, {stdio: 'inherit'})

		// Create a pull request with the changes
		const octokit = github.getOctokit(core.getInput("github-token"))
		octokit.rest.pulls.create({
			...context.repo,
			head: branchName,
			base: "master",
			maintainer_can_modify: true,
			title: `Update ${manifest.name} to ${latestVersion}`,
		})

		// Switch back to master branch
		execSync(`git checkout master`, {stdio: 'inherit'})
	}

} catch (error) {
	core.setFailed(error)
}

function getVersionFromPKGBUILD(dir: string): string | undefined {
	const fileContents: string = fs.readFileSync(path.join(dir, "PKGBUILD")).toString()

	const matches = fileContents.match(/^pkgver=(.*)$/m)
	if (matches === null) {
		return undefined
	}

	return matches[0]
}

async function getLatestVersionFromGithub(repo: string): Promise<string | undefined> {
	const split = repo.split("/")
	const owner = split[0]
	const repoName = split[1]

	if (owner === undefined || repoName === undefined) {
		return undefined
	}

	const octokit = github.getOctokit(core.getInput("github-token"))

	const resp = await octokit.rest.repos.getLatestRelease({
		owner: owner,
		repo: repoName,
	})

	if (resp.status !== 200) {
		return undefined
	}

	return resp.data.tag_name
}

interface IManifest {
	name: string,
	testCmd: string | null,
	include: string[],
	automaticUpdates: {
		type: string,
		repo: string,
	}
}
