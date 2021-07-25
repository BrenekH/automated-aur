import * as core from "@actions/core";
import { promise as glob } from "glob-promise";

try {
	// Identify all packages in the pkgs directory
	const manifests = await glob("pkgs/**/.aurmanifest.json")

	manifests.forEach((manifestPath) => {
		core.info(manifestPath)

		// TODO: Run a check for updates according to .aurmanifest.json
		// TODO: Open a PR with updates
	})

} catch (error) {
	core.setFailed(error);
}
