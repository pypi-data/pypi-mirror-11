## v0.3.2
* Pin docker-compose to v1.3.1.
+ Add files section to setup.cfg.

## v0.3.1
* Fix /bin/echo bug.

## v0.3.0
* Replace fig with docker-compose.

## v0.2.2
* Fix pushing 'latest' tag.

## v0.2.1
* Now git SHA version tags are uppercase.

## v0.2.0 - First
+ Allow tagging a single build with multiple versions.
+ Allow config file to be named `.container.yml`.
+ Manage 'latest' images.
+ Add tests for Docker functionality.
* Convert README to RST.
* Fix rm command. 
* Add minimal filter support to value substitution.

## v0.1.4 - Info Bug Fix
* Fix info command failure when fig.yml does not exist.

## v0.1.3 - Version Verification
+ Support version verification on build, push, run, and test commands.
* Catch OSErrors for subprocess calls.
* Minor code cleanup.

## v0.1.2 - CI Bug Fix
* Cover more container removal cases for CI.

## v0.1.1 - Test Bug Fixes
* Run all containers during test.
* Make test rebuild option functional.

## v0.1.0 - Test Command
+ Support running a test container.
+ Add config directive `testing`.
* Changed config directive `fig` to `running`.
* Changed info key `built` to `is-built`.
* Changed info key `running` to `is-running`.

## v0.0.2 - Bug Fixes
+ Add hack for running under CircleCI.
+ Handle KeyboardInterrupts gracefully.
+ Require fig as a dependency.

## v0.0.1 - Initial Alpha Release
+ Support build, info, push, rm, and run commands.
+ Support prebuild scripts.
+ Support version detection.
