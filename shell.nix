with import <nixpkgs> {};
with pkgs.python39Packages;
( let
  bibot_package = buildPythonPackage rec {
    name = "bibot";
    src = ./.;
    propagatedBuildInputs = [setuptools pytest pkgs.libsndfile ];
  };
in
  pkgs.python39.buildEnv.override rec {
    extraLibs = [
      bibot_package
      pytest
      selenium
      beautifulsoup4
      pandas
      pudb
      jedi
    ];
  }
  ).env
