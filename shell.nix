with import <nixpkgs> {};
with pkgs.python39Packages;
let
  bibot_package = buildPythonPackage rec {
    name = "bibot";
    src = ./.;
    propagatedBuildInputs = [setuptools pytest pkgs.libsndfile ];
  };
  dev_packages = python-packages: with python-packages; [
    bibot_package
    pytest

    selenium
    beautifulsoup4
    pudb
    jedi
  ];
  bibot_python = python39.withPackages dev_packages;
in
  mkShell {
    nativeBuildInputs = [
      bibot_python
    ];
    buildInputs = [bibot_python];
  }
