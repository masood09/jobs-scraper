{
  description = "A simple Python development environment for jobscraper-python";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.python3
            pkgs.python3Packages.virtualenv
          ];

          shellHook = ''
            echo "Setting up Python environment..."
            python3 -m venv .venv
            source .venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements/dev.txt
            echo "Environment ready! Run 'python scripts/run.py dev' to start the service."
          '';
        };
      }
    );
}
