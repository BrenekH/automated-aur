import * as core from "@actions/core";
import * as github from "@actions/github";
import { PullRequest } from "@octokit/webhooks-definitions/schema";

try {

	const context = github.context;
	if (context.eventName !== "pull_request") {
		throw "Not a pull request";
	}

	const pr = context.payload.pull_request as PullRequest;
	const octokit = github.getOctokit(core.getInput("token"));

	// octokit.auth;

	// console.log(pr);

	console.log(pr.diff_url.replace("https://github.com", ""));

	octokit.request(pr.diff_url.replace("https://github.com", ""), {headers: {Accept: "application/vnd.github.v3.diff"}}).then((value) => {
		console.log(value);
	}).catch((error) => {
		core.setFailed(error);
	});

	console.log(pr.patch_url.replace("https://github.com", ""));

	octokit.request(pr.patch_url.replace("https://github.com", ""), {headers: {Accept: "application/vnd.github.v3.patch"}}).then((value) => {
		console.log(value);
	}).catch((error) => {
		core.setFailed(error);
	});

} catch (error) {
	core.setFailed(error);
}
