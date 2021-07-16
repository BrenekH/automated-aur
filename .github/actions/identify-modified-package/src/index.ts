import * as core from "@actions/core";

try {
	console.log("Hello, World!")
} catch (error) {
	core.setFailed(error);
}
