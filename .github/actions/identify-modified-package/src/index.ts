import * as core from "@actions/core";
import * as github from "@actions/github";

try {
	console.log(github.context);
} catch (error) {
	core.setFailed(error);
}
