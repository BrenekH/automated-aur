import * as core from "@actions/core";
import * as github from "@actions/github";
// import { PullRequest } from "@octokit/webhooks-definitions/schema";

try {

	const context = github.context;
	if (context.eventName !== "pull_request") {
		throw "Not a pull request";
	}

	// const pr = context.payload.pull_request as PullRequest;
	const octokit = github.getOctokit(core.getInput("token"));

	octokit.rest.pulls.listFiles({
		...context.repo,
		pull_number: context.payload.pull_request?.number as number,
	}).then((value) => {
		console.log(value);
	}).catch((error) => {
		core.setFailed(error);
	});

} catch (error) {
	core.setFailed(error);
}
