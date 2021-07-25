import * as core from "@actions/core";
import * as github from "@actions/github";
import { promise as glob } from "glob-promise";
import * as fs from "fs";
import * as path from "path";

try {
	// Identify all packages in the pkgs directory
	const manifests = await glob("pkgs/**/.aurmanifest.json")

	for (const manifestPath of manifests) {
		core.info(manifestPath)

		const manifest = JSON.parse(fs.readFileSync(manifestPath).toString()) as IManifest;

		const pkgbuildVersion: string | undefined = getVersionFromPKGBUILD(manifestPath.replace("/.aurmanifest.json", ""))
		if (pkgbuildVersion === undefined) {
			core.warning(`Unable to get package version from PKGBUILD (${manifest.name})`);
			continue;
		}

		let latestVersion = "";
		switch (manifest.automaticUpdates.type) {
			case "github":
				const ghVersion = await getLatestVersionFromGithub(manifest.automaticUpdates.repo);
				if (ghVersion === undefined) {
					core.warning(`Failed to get latest version from GitHub (${manifestPath}).`);
					continue;
				}
				latestVersion = ghVersion;
				break;
			default:
				core.warning(`Unknown automaticUpdates type '${manifest.automaticUpdates}' in ${manifestPath}`);
				continue;
		}

		if (pkgbuildVersion === latestVersion) {
			continue;
		}

		// TODO: Open a PR with updates
	}

} catch (error) {
	core.setFailed(error);
}

function getVersionFromPKGBUILD(dir: string): string | undefined {
	const fileContents: string = fs.readFileSync(path.join(dir, "PKGBUILD")).toString();

	const matches = fileContents.match(/^pkgver=(.*)$/m);
	if (matches === null) {
		return undefined;
	}

	return matches[0];
}

async function getLatestVersionFromGithub(repo: string): Promise<string | undefined> {
	const split = repo.split("/");
	const owner = split[0];
	const repoName = split[1];

	if (owner === undefined || repoName === undefined) {
		return undefined;
	}

	const octokit = github.getOctokit(core.getInput("github-token"));

	const resp = await octokit.rest.repos.getLatestRelease({
		owner: owner,
		repo: repoName,
	})

	if (resp.status !== 200) {
		return undefined;
	}

	return resp.data.tag_name;
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
