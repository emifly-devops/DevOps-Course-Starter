Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update && sudo apt-get upgrade
    sudo apt-get install -y make \
                            build-essential \
                            libssl-dev \
                            zlib1g-dev \
                            libbz2-dev \
                            libreadline-dev \
                            libsqlite3-dev \
                            wget \
                            curl \
                            llvm \
                            libncursesw5-dev \
                            xz-utils \
                            tk-dev \
                            libxml2-dev \
                            libxmlsec1-dev \
                            libffi-dev \
                            liblzma-dev

    rm ~/.bashrc
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    echo -e '\n# pyenv setup' >> ~/.profile
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'command -v pyenv >/dev/null || export PATH="$PATH:$PYENV_ROOT/bin"' >> ~/.profile
    echo 'eval "$(pyenv init -)"' >> ~/.profile

    echo -e '\n# poetry setup' >> ~/.profile
    echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.profile

    source ~/.profile

    pyenv install 3.10.7
    pyenv global 3.10.7

    nvm install 16.17.1
    nvm alias default 16.17.1

    curl -sSL https://install.python-poetry.org | python -
  SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the todo app setup script"
    trigger.run_remote = {privileged: false, inline: "
      cd /vagrant

      npm install
      poetry install

      nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
    "}
  end
end
