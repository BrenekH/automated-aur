import * as core from "@actions/core";
import * as github from "@actions/github";
import { PullRequest } from "@octokit/webhooks-definitions/schema";

try {

	console.log(github.context);
	if (github.context.eventName !== "pull_request") {
		throw "Not a pull request";
	}

	const pr = github.context.payload as PullRequest;
	const octokit = github.getOctokit(core.getInput("token"));

	console.log(pr.patch_url);

	octokit.request(pr.patch_url).then((value) => {
		console.log(value);
	}).catch((error) => {
		core.setFailed(error);
	});

} catch (error) {
	core.setFailed(error);
}
