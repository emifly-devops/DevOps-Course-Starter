Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "shell", inline: <<-SHELL
    echo "=== INSTALL KEY DEPENDENCIES ==="

    apt-get update && apt-get upgrade
    apt-get install -y make \
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

    echo "=== INSTALL NODE AND NPM USING NVM ==="

    export NVM_DIR="/opt/nvm" && (
      git clone https://github.com/nvm-sh/nvm.git $NVM_DIR
      cd $NVM_DIR
      git checkout `git describe --abbrev=0 --tags --match "v[0-9]*" $(git rev-list --tags --max-count=1)`
    ) && source $NVM_DIR/nvm.sh

    nvm install 16.17.1

    ln -s $NVM_DIR/versions/node/v$(cat $NVM_DIR/alias/default)/bin/node /usr/local/bin/node
    ln -s $NVM_DIR/versions/node/v$(cat $NVM_DIR/alias/default)/bin/npm /usr/local/bin/npm

    echo "=== INSTALL PYTHON AND POETRY USING PYENV ==="

    export PYENV_ROOT="/opt/pyenv" && (
      git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT
      ln -s $PYENV_ROOT/bin/pyenv /usr/local/bin/pyenv
      eval "$(pyenv init -)"
    )

    pyenv install 3.10.7
    pyenv global 3.10.7

    ln -s $PYENV_ROOT/shims/python /usr/local/bin/python

    export POETRY_HOME="/opt/poetry" && (
      curl -sSL https://install.python-poetry.org | python -
    )

    ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry
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
