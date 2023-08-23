# CHANGELOG

## v0.7.1 (2023-08-23)

### Fix

* fix: disk check on nvme based firewalls fixes #1 ([`c51d12e`](https://github.com/TeraIT-at/check_paloalto_ng/commit/c51d12ef6ecaa3e046f5ded93c3bb78cb79c19b7))

## v0.7.0 (2023-01-27)

### Chore

* chore: update README ([`fea23a5`](https://github.com/TeraIT-at/check_paloalto_ng/commit/fea23a53da4cb484510610fb01686dbf01669eab))

### Fix

* fix: line-endings ([`d47e491`](https://github.com/TeraIT-at/check_paloalto_ng/commit/d47e49178ff2d0702c1ce222fbf067d614bb6fd8))

* fix: authors after merge conflicts ([`f3c8c9a`](https://github.com/TeraIT-at/check_paloalto_ng/commit/f3c8c9a23430eb90726d68a39da28173379f4aeb))

* fix: update diskspace parsing ([`b87825d`](https://github.com/TeraIT-at/check_paloalto_ng/commit/b87825d942183c440c16b21eea5ea227b70e4f08))

### Unknown

* Merge remote-tracking branch &#39;fork2/master&#39; ([`f07180a`](https://github.com/TeraIT-at/check_paloalto_ng/commit/f07180a080c0aa17917012300b4f4a71865d9f63))

* Merge remote-tracking branch &#39;fork1/master&#39;

# Conflicts:
#	AUTHORS.rst
#	CONTRIBUTING.rst
#	check_pa/__init__.py
#	check_pa/check_paloalto.py
#	setup.py ([`1741a54`](https://github.com/TeraIT-at/check_paloalto_ng/commit/1741a54276f0cd63153a24b9ceca14bf0086a506))


## v0.6.0 (2023-01-26)

### Chore

* chore: add readthedocs.yml ([`0d97088`](https://github.com/TeraIT-at/check_paloalto_ng/commit/0d97088d327873bab9d22beb29bbd76c9b71b77b))

### Feature

* feat: add additional checks from @frank-m
https://github.com/frank-m/nagios_check_paloalto/tree/add_additional_checks
Merge remote-tracking branch &#39;https://github.com/frank-m/nagios_check_paloalto/tree/add_additional_checks&#39; ([`4ff9662`](https://github.com/TeraIT-at/check_paloalto_ng/commit/4ff966288062adac631e8f8ce355b4eb7457ab70))


## v0.5.1 (2023-01-26)

### Chore

* chore: update docs ([`af579d9`](https://github.com/TeraIT-at/check_paloalto_ng/commit/af579d9325f9fe5b60a14adc04b6d3983bc23403))

### Feature

* feat: license check ([`38b4c51`](https://github.com/TeraIT-at/check_paloalto_ng/commit/38b4c5191bb25b3d56d6f69d536c37605d96d60f))


## v0.4.1 (2022-04-25)

### Fix

* fix: usage ([`4038e54`](https://github.com/TeraIT-at/check_paloalto_ng/commit/4038e54305154f228c30e32c7d9ce5a332f57467))


## v0.4.0 (2022-04-25)

### Chore

* chore: update docs &amp; branding, push requirements ([`ff91079`](https://github.com/TeraIT-at/check_paloalto_ng/commit/ff91079932567f328743db5ac3adf1f7509fb9a3))

### Feature

* feat: add tests for new checks &amp; clean up old tests ([`7f4d661`](https://github.com/TeraIT-at/check_paloalto_ng/commit/7f4d6619ccad80cc024916e0a90782aaacafa07a))

* feat: pppoe interface check ([`0dfa67c`](https://github.com/TeraIT-at/check_paloalto_ng/commit/0dfa67c64ae14ca8be75a656bbf08e95c030998d))

* feat: power supply check ([`f2d52db`](https://github.com/TeraIT-at/check_paloalto_ng/commit/f2d52db4c9045eaaa0f6bd4d9f9f472a9ec40d1d))

### Fix

* fix: improve new check outputs ([`2ceaeb2`](https://github.com/TeraIT-at/check_paloalto_ng/commit/2ceaeb2ce10e6da7fba7810c75dfb147e0d87e51))

### Unknown

* replaced too much ([`da99740`](https://github.com/TeraIT-at/check_paloalto_ng/commit/da99740f8a51490af37ea13e89f77bdba97553fb))

* add blank lines ([`7f7e1d5`](https://github.com/TeraIT-at/check_paloalto_ng/commit/7f7e1d51dfc3c7bcac05c067d0d338ef75420887))

* add else for positive return ([`a091a64`](https://github.com/TeraIT-at/check_paloalto_ng/commit/a091a6438de47603f5c64318878fd62610c35635))

* Add interface check ([`7727c74`](https://github.com/TeraIT-at/check_paloalto_ng/commit/7727c74224df85371ca383cb47730b1ce27479d6))

* add license expiry check ([`f44729e`](https://github.com/TeraIT-at/check_paloalto_ng/commit/f44729ea77d94911c6044aa92377ebff8f3483ce))

* fix naming and check connection up ([`9ccc111`](https://github.com/TeraIT-at/check_paloalto_ng/commit/9ccc11125ee181ea687af11bfb244e09cc673080))

* add configuration sync enabled and sync status ([`2f0fb92`](https://github.com/TeraIT-at/check_paloalto_ng/commit/2f0fb9242b5ff6d9454ec591a18ddfc27ac95d7f))

* also check configuration sync ([`76f2756`](https://github.com/TeraIT-at/check_paloalto_ng/commit/76f2756d4b38eca7f519ded493a83e0977fae94f))

* add_cluster_check ([`1ac3414`](https://github.com/TeraIT-at/check_paloalto_ng/commit/1ac3414976c4b75865a46f2de8d88ab634b0cb14))

* Aggregate same results

Signed-off-by: Rémi VERCHERE &lt;remi.verchere@axians.com&gt; ([`9f39e52`](https://github.com/TeraIT-at/check_paloalto_ng/commit/9f39e52c4870e92a0b0865f951a5ef602c3baae7))

* Correct link to reports

Signed-off-by: Rémi VERCHERE &lt;remi.verchere@axians.com&gt; ([`7733010`](https://github.com/TeraIT-at/check_paloalto_ng/commit/773301024b2e1cbfdc64fa1e21d9eee8a5591a28))

* Correct return values

Signed-off-by: Rémi VERCHERE &lt;remi.verchere@axians.com&gt; ([`72a9857`](https://github.com/TeraIT-at/check_paloalto_ng/commit/72a9857fc44f7380801f2211859f83e8c8b037c3))

* Add reports ([`a1883c0`](https://github.com/TeraIT-at/check_paloalto_ng/commit/a1883c07a2b90da4861f7f8f90f03318aaf396e7))

* commit untracked changes

Signed-off-by: Rémi VERCHERE &lt;remi.verchere@axians.com&gt; ([`2eb8063`](https://github.com/TeraIT-at/check_paloalto_ng/commit/2eb8063446e32a04f8dfcf0c094982c2728db1a8))

* WIP: get QoS information

Signed-off-by: Rémi VERCHERE &lt;remi.verchere@axians.com&gt; ([`ac1f762`](https://github.com/TeraIT-at/check_paloalto_ng/commit/ac1f7626356751101bc55bf7d9aa9132646bbefe))

* Update check_paloalto.py

Added + argument : -A -agent : You can check the agent name if you want. Exmaple: all ([`e0e207f`](https://github.com/TeraIT-at/check_paloalto_ng/commit/e0e207f41f5c2fb828d2bae78fbf5a52c198231c))

* Update useragent.py

Added + argument -A --agent : You need define what is the agent name. Example. all ([`dc04e0c`](https://github.com/TeraIT-at/check_paloalto_ng/commit/dc04e0cf068a5f4f8bf218c9567e2d98c2d1319e))

* Update useragent.py ([`266b78a`](https://github.com/TeraIT-at/check_paloalto_ng/commit/266b78a7437744a89998b3f657f77fdf3ad421ec))

* Update LICENSE ([`6c439d8`](https://github.com/TeraIT-at/check_paloalto_ng/commit/6c439d87a5706c6ab97df39258699835040973e0))

* Merge branch &#39;bgp&#39; ([`adb6d88`](https://github.com/TeraIT-at/check_paloalto_ng/commit/adb6d88587bb057ba0a0e317949e76d884a05eab))

* Trying to correct bgp tests ([`1e13b22`](https://github.com/TeraIT-at/check_paloalto_ng/commit/1e13b229878e0dc55909d0312b8ccb43416ea333))

* Ad BGP tests ([`5cfdc2f`](https://github.com/TeraIT-at/check_paloalto_ng/commit/5cfdc2f8c7841e20eecb4408fa8b05b02f4a8cc7))

* Ad BGP tests ([`b1b6740`](https://github.com/TeraIT-at/check_paloalto_ng/commit/b1b6740b61bac2a9c91ce49b60719fcd6d0d269c))

* Add BGP Peer status duration ([`c53e5dd`](https://github.com/TeraIT-at/check_paloalto_ng/commit/c53e5dd525fd68c72b7ffdaf20b651e5e87688cf))

* Add BGP Peer Context ([`7818dd1`](https://github.com/TeraIT-at/check_paloalto_ng/commit/7818dd1fb089f3ddc144f5c2dee7fdd8f7867c46))

* Add BGP Peer Context ([`ba66a9b`](https://github.com/TeraIT-at/check_paloalto_ng/commit/ba66a9bc5752346c0b40cba2e7d67afd75d58ac6))

* Correct BGP ([`36a62e7`](https://github.com/TeraIT-at/check_paloalto_ng/commit/36a62e759df80894283e10ce1bff7a1b5d8aa1ec))

* Add peer status ([`906cefc`](https://github.com/TeraIT-at/check_paloalto_ng/commit/906cefcee1e8deb60a031da6f5f2d4ce1b319611))

* BGP negative check ([`7bc0f8a`](https://github.com/TeraIT-at/check_paloalto_ng/commit/7bc0f8af35d1dcfdda170734b7273bf3a81792e3))

* Add BGP modes ([`4776313`](https://github.com/TeraIT-at/check_paloalto_ng/commit/47763132f4442fc43aa2d033d3f8ff44bcab3ddf))

* Correct BGP check ([`6417a6e`](https://github.com/TeraIT-at/check_paloalto_ng/commit/6417a6e6c1f1bd0ac6f173c57a37bee0a9f018b9))

* Add BGP informations ([`0146b26`](https://github.com/TeraIT-at/check_paloalto_ng/commit/0146b2670c204c09d609a6bf6edcfaa7b9ecb462))

* Update readme ([`17f8363`](https://github.com/TeraIT-at/check_paloalto_ng/commit/17f836330d231d18d0a616d18379f66edbfba29b))

* Play with travis ([`b9f806a`](https://github.com/TeraIT-at/check_paloalto_ng/commit/b9f806a1cc7a410151fc7863c23a8d2d49866aae))

* Incorrect copy/paste ([`9b81356`](https://github.com/TeraIT-at/check_paloalto_ng/commit/9b81356fbdbca530019aa6b0722da6327df32525))

* Fix threat summary typo ([`652f8f2`](https://github.com/TeraIT-at/check_paloalto_ng/commit/652f8f29daf55d8ca86e5b5f1b4512f54b1c67e0))

* Add threat date ([`cbec44e`](https://github.com/TeraIT-at/check_paloalto_ng/commit/cbec44e1e958cf1786891e64b20b9352baba8d98))

* AV add warn/crit ([`ee1ffee`](https://github.com/TeraIT-at/check_paloalto_ng/commit/ee1ffee8cec4277afea85bf89c452ffe3795961c))

* AV correct infos ([`049ca56`](https://github.com/TeraIT-at/check_paloalto_ng/commit/049ca56e44dfb863456d3ad67a650e2fab811076))

* AV return difference days ([`948abf3`](https://github.com/TeraIT-at/check_paloalto_ng/commit/948abf30e70b1dd0ed06817c5556ab6b740e0117))

* Invert date check ([`1c89f87`](https://github.com/TeraIT-at/check_paloalto_ng/commit/1c89f87ebe35708b6beff47a33a7462ac7f806f9))

* Add AV datetime ([`9439052`](https://github.com/TeraIT-at/check_paloalto_ng/commit/9439052b210db8759fd755465345d44e4744f368))

* Add AV difference time ([`480472d`](https://github.com/TeraIT-at/check_paloalto_ng/commit/480472d83042b31104672d55b88204ce853be8af))

* Incorrect AV init ([`c9ce900`](https://github.com/TeraIT-at/check_paloalto_ng/commit/c9ce90047bfb21995ca7d6e9698e208410323dc8))

* Fix parser AV ([`43cf2cb`](https://github.com/TeraIT-at/check_paloalto_ng/commit/43cf2cb45d641889d23b42a3949827f1de31ce7e))

* Correct AV vars ([`8e21065`](https://github.com/TeraIT-at/check_paloalto_ng/commit/8e21065441647105b3bc41f18d028561f0a8ea5e))

* Finder output str and int ([`a963c7f`](https://github.com/TeraIT-at/check_paloalto_ng/commit/a963c7f97b785da493837b5cef7145455eeea9ef))

* Add Antivirus informations ([`c9953ac`](https://github.com/TeraIT-at/check_paloalto_ng/commit/c9953ac22c03885d0594351f9b85ce1f9574977a))

* Check throughput to all interfaces

Update gitignore with virtualenv dirs

Add warning and critical thresholds for throughput

Correct tests throughput with thresholds and update travis config ([`04f72b8`](https://github.com/TeraIT-at/check_paloalto_ng/commit/04f72b8219b8e92653eb9f827f34e582bc5d386c))

* Release 0.3.2 ([`3955891`](https://github.com/TeraIT-at/check_paloalto_ng/commit/39558916b84a717bfed3b8027fcff764335018a8))

* Release 0.3.1 ([`98d0a51`](https://github.com/TeraIT-at/check_paloalto_ng/commit/98d0a517dd7f7bc9d96082b436154984815e1389))

* Merge remote-tracking branch &#39;origin/master&#39; ([`5664a89`](https://github.com/TeraIT-at/check_paloalto_ng/commit/5664a8993aabf89f7814733948bfb29f5413fe71))

* Release 0.3 ([`5f7be0e`](https://github.com/TeraIT-at/check_paloalto_ng/commit/5f7be0e6e2b96694d5cd7c1640ca4dc12ea48090))

* Update README.rst ([`c1a980c`](https://github.com/TeraIT-at/check_paloalto_ng/commit/c1a980c3622f6c381ed79394a53fc173a2e8b601))

* Change testing in Travis-CI to tox ([`08345e6`](https://github.com/TeraIT-at/check_paloalto_ng/commit/08345e669921d78b5a1b3bbb90e657e4df980a35))

* Support for python 3.5 added ([`0dcb240`](https://github.com/TeraIT-at/check_paloalto_ng/commit/0dcb2404c4fbca5aaff079b12041df0140d8c63b))

* Minor code improvements ([`f92cf5a`](https://github.com/TeraIT-at/check_paloalto_ng/commit/f92cf5a52627b4ac71e5ef1307ce54e30ba526da))

* Minor setup changes ([`da1362e`](https://github.com/TeraIT-at/check_paloalto_ng/commit/da1362ecea7212145262e869a3fdce871ceae3d3))

* Added vagrant development environment ([`b551180`](https://github.com/TeraIT-at/check_paloalto_ng/commit/b551180d0034f23d1ba38fa2bef2776a2f8797e2))

* Updated installation command. ([`2e4b0dc`](https://github.com/TeraIT-at/check_paloalto_ng/commit/2e4b0dca6dcf5834598873601f6f247de9fda8b2))

* Last changes for release 0.1.6. ([`26577f6`](https://github.com/TeraIT-at/check_paloalto_ng/commit/26577f6b4e6948feb73ce12fa8082ce7c0bc9f55))

* Changes for release 0.1.6. ([`ab814e1`](https://github.com/TeraIT-at/check_paloalto_ng/commit/ab814e1b56dd7ea736110deb09ea8ccfa779ab15))

* Changes for release 0.1.6. ([`561e818`](https://github.com/TeraIT-at/check_paloalto_ng/commit/561e81817054f54d20fd5e5e3109a59b5428fdac))

* Minor changes for release 0.1.5. ([`3008cfb`](https://github.com/TeraIT-at/check_paloalto_ng/commit/3008cfb2cac08401af8e3474d4d13df925504085))

* Changelog for upcoming release 0.1.4. ([`dad0c8c`](https://github.com/TeraIT-at/check_paloalto_ng/commit/dad0c8cc99d67e6501afad1dd389f9cf4058dada))

* Changed tox config and cleanup ([`bb4e73d`](https://github.com/TeraIT-at/check_paloalto_ng/commit/bb4e73d4f2ad07d6551fef8224ba489584fd8c77))

* Added some docs ([`4de8185`](https://github.com/TeraIT-at/check_paloalto_ng/commit/4de8185eab52ef2faf5715baf4b3068e40343290))

* Improved sessinfo command ([`d47b6f8`](https://github.com/TeraIT-at/check_paloalto_ng/commit/d47b6f82ea1c4c7de0d635804fc76cd5348109a6))

* Merge remote-tracking branch &#39;origin/development&#39; into development ([`d80f2f6`](https://github.com/TeraIT-at/check_paloalto_ng/commit/d80f2f623ed8e59188fa5111da820039d39bda6a))

* Improved error handling a bit when upgrading or resetting PA ([`bc2a8e2`](https://github.com/TeraIT-at/check_paloalto_ng/commit/bc2a8e20b230a8ed4146f71713a6037c482d1cfc))

* Improved error handling a bit when upgrading or resetting PA ([`f3c5131`](https://github.com/TeraIT-at/check_paloalto_ng/commit/f3c513170fd00c65c58aa04469c5d81d56538137))

* Added useragent functionality. ([`91c20af`](https://github.com/TeraIT-at/check_paloalto_ng/commit/91c20af1ded500a280fc1fc2fc993728c9e62cd5))

* Added script timeout switch ([`2ad2669`](https://github.com/TeraIT-at/check_paloalto_ng/commit/2ad26690c87f7c830840e1f88e82958a2d493a32))

* first attempt to a check for running user-agents ([`1257f39`](https://github.com/TeraIT-at/check_paloalto_ng/commit/1257f39a6a00984c73184c2fe7529d12b51baade))

* updated docs ([`22e2ebd`](https://github.com/TeraIT-at/check_paloalto_ng/commit/22e2ebd244877dc30811dc31889bd318cebcabae))

* Release 0.1.3: Disabled warnings for insecure requests to support older installations:
  https://urllib3.readthedocs.org/en/latest/security.html ([`af52671`](https://github.com/TeraIT-at/check_paloalto_ng/commit/af5267192d38c7f9c6fc2fa9aba747bd42d869f0))

* Release 0.1.2 ([`f384343`](https://github.com/TeraIT-at/check_paloalto_ng/commit/f384343dd701c86f50dc50ba943a167405d3d583))

* Require updated wheel. ([`a35e190`](https://github.com/TeraIT-at/check_paloalto_ng/commit/a35e1907aea5ffa66669e0969db113476e0f106b))

* Updated docs. ([`cf8fdee`](https://github.com/TeraIT-at/check_paloalto_ng/commit/cf8fdeebe285a1594a7791a84ccac4375e0f719e))

* Updated Wheel cfg file. ([`54a6402`](https://github.com/TeraIT-at/check_paloalto_ng/commit/54a64026d67061c60a79c3ef00afac3f9e23c364))

* Fixed different behaviour for parsing args in python3. ([`ec6c524`](https://github.com/TeraIT-at/check_paloalto_ng/commit/ec6c5249208dc5b5fa5115801ef8892d90a093ed))

* Enabled warnings for insecure platform: https://urllib3.readthedocs.org/en/latest/security.html ([`b2a3cb3`](https://github.com/TeraIT-at/check_paloalto_ng/commit/b2a3cb301cf88cb958d527f884ddb7bee8dcfc69))

* Removed unused section. ([`c3a0406`](https://github.com/TeraIT-at/check_paloalto_ng/commit/c3a0406ec11b4d65bd66276188aeb349c4af139f))

* Release 0.1.1 ([`cd4ec0a`](https://github.com/TeraIT-at/check_paloalto_ng/commit/cd4ec0afbf96276ba32a789f239b51a4f45da6f7))
