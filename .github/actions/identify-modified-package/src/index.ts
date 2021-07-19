import * as core from "@actions/core";
import * as github from "@actions/github";
// import { PullRequest } from "@octokit/webhooks-definitions/schema";

try {

	const context = github.context;
	if (context.eventName !== "pull_request") {
		throw "Not a pull request";
	}

	// const pr = context.payload.pull_request as PullRequest;
	const octokit = github.getOctokit(core.getInput("github-token"));

	const resp = await octokit.rest.pulls.listFiles({
		...context.repo,
		pull_number: context.payload.pull_request?.number as number,
	})

	let moddedPackages: string[] = [];
	resp.data.forEach((file) => {
		const splitFName = file.filename.split("/");
		if (splitFName[0] === "pkgs") {
			const splicedString = `${splitFName[0]}/${splitFName[1]}`;
			if (moddedPackages.indexOf(splicedString) === -1) moddedPackages.push(splicedString)
		}
	});

	if (moddedPackages.length > 1) {
		throw "More than one modified package.";
	}

	core.setOutput("package", moddedPackages[0]);

} catch (error) {
	core.setFailed(error);
}
