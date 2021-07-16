import * as core from "@actions/core";
import * as github from "@actions/github";
import { PullRequest } from "@octokit/webhooks-definitions/schema";

try {

	const pr = github.context.payload as PullRequest;
	const octokit = github.getOctokit(core.getInput("token"));

	console.log(pr.patch_url);

	console.log(octokit.request(pr.patch_url));

} catch (error) {
	core.setFailed(error);
}
