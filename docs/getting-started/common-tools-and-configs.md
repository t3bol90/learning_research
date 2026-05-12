# Common tools and configurations

## 1. Shell configuration

Using zsh as the default shell works well.

First, install oh-my-zsh, which is the management tool for zsh:
[https://github.com/ohmyzsh/ohmyzsh](https://github.com/ohmyzsh/ohmyzsh)

Then install plugins:

1. Copy the shell config between machines: [https://github.com/rutchkiwi/copyzshell](https://github.com/rutchkiwi/copyzshell)

    If a machine already has an oh-my-zsh setup and a new machine needs configuring, and zsh is already available, you do not need to repeat the steps below (do not install oh-my-zsh on the new machine, just transfer the config across, because once it is installed it cannot be overwritten directly and that gets messy). Just transfer it. If you need to add the machine port, see the issue.

2. Command highlighting and command syntax checking (must install): [https://github.com/zsh-users/zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)

    Note: use the oh-my-zsh install method shown there, since it is easier to migrate.

3. Auto-suggestion (must install): [https://zhuanlan.zhihu.com/p/111707433](https://zhuanlan.zhihu.com/p/111707433)

    When the suggestion shows the line you want, press Ctrl+F to accept it.

    If you want to see all options: pressing Tab once only shows the options but you still have to type them in by hand. Pressing Tab twice lets you pick directly with the arrow keys.

4. fzf with history (must install).

Manually switch the default shell:

```shell
cat /etc/shells  # list all shells

echo $SHELL      # show the shell currently in use

chsh -s /usr/bin/zsh  # change the default shell
```

If you need a password to change the default shell and you do not know the password, a good workaround is to add the line `zsh` to the end of `~/.bashrc`. That way zsh starts automatically, and on launch it runs `~/.zshrc` once.

## Some commonly used tools

- ncdu: `apt-get install ncdu`. Shows folder usage.
- nvtop. If it does not install, use nvitop (install from GitHub into the Python environment).
- fzf: also has some usage notes.
- ctop: monitors resource usage of each Docker container (needs sudo).
- tmux: see below.
- vim: see below.

## tmux configuration

Add mouse support in tmux:

```shell
touch ~/.tmux.conf
echo "set -g mouse on" >> ~/.tmux.conf

# If the line above does not work, first add the following to ~/.tmux.conf:
setw -g mode-mouse on
setw -g mouse-resize-pane
setw -g mouse-select-pane
setw -g mouse-select-window
set-option -g history-limit 5000

# Then:
tmux source-file ~/.tmux.conf
```

A handy all-in-one tmux config (strongly recommended):
[https://github.com/samoshkin/tmux-config](https://github.com/samoshkin/tmux-config)

Needs tmux version greater than 2.4. Check the version with `tmux -V`. 2.1 also works in practice.

You still need to run `tmux source-file xx`.

If there is a syntax error, see:
[https://github.com/samoshkin/tmux-config/issues/38](https://github.com/samoshkin/tmux-config/issues/38)

## vim configuration

[https://github.com/amix/vimrc](https://github.com/amix/vimrc)

`ssh-keygen -t rsa`

```shell
vim ~/.vimrc
set nu   # add "set nu" in vimrc to show line numbers
let g:snipMate = { 'snippet_version' : 1 } # add this at the end of vimrc to stop vim from throwing the "decrepit" message on startup
```

Add a file tree to vim:
[https://github.com/preservim/nerdtree](https://github.com/preservim/nerdtree)

Then add automatic open and close of NERDTree:
[https://riptutorial.com/vim/example/30660/nerd-tree](https://riptutorial.com/vim/example/30660/nerd-tree)

If you want the cursor to land in the current file after the tree opens, use this command instead of the one in the link:

```vim
" Start NERDTree and put the cursor back in the other window.
autocmd VimEnter * NERDTree | wincmd p
```

## 2. Anaconda / Miniconda download and configuration

Anaconda:

```shell
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2019.10-Linux-x86_64.sh
```

If that is too slow, use Miniconda:
[https://repo.anaconda.com/miniconda/](https://repo.anaconda.com/miniconda/)

```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh
```

Pick the version you want from there and swap the Anaconda path for the one you want.

Install and refresh:

```shell
zsh Anaconda3-2019.10-Linux-x86_64.sh

source ~/.zshrc
```

Replace the file name with the one you downloaded.

If conda commands are still missing after that, then it has been installed under bashrc. Run `vi ~/.bashrc`, find all the related lines, copy them into `~/.zshrc`, and source again.

### 2.1 conda environment commands

[https://blog.csdn.net/hejp_123/article/details/92151293](https://blog.csdn.net/hejp_123/article/details/92151293)

Create a new environment:

```shell
conda create --name your_env_name python=3.6
```

Create a new environment from a YAML file:

```shell
conda env create -f filepath.yaml
```

Remove an environment:

```shell
conda remove -n your_env_name --all

conda remove --name your_env_name --all
```

Use a domestic conda mirror to speed things up:

```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

Use a company conda mirror to speed things up:
[https://dx-mirrors.sensetime.com/help/use-conda-mirror.html](https://dx-mirrors.sensetime.com/help/use-conda-mirror.html)

### 2.2 pip with a custom index

```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tensorboard
```

**Note:** check that the pip in use is the one inside the current conda environment:

```shell
which pip
# if not (it falls out of the env quite often)
conda deactivate
conda activate
which pip
```

If pip was installed via conda, then pip and conda are linked, and they can find each other's installed packages.

```shell
# update package
pip install -U name
```

Use a domestic pip mirror to speed things up:

```text
1. Temporary setting:

When you run pip, append the parameter -i https://pypi.tuna.tsinghua.edu.cn/simple

For example: pip install jieba -i https://pypi.tuna.tsinghua.edu.cn/simple  # jieba is a package

2. Permanent setting:

pip install pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

After that, install packages as you normally would. The speed goes up many times over.

For example: pip install jieba

Switch to Aliyun for the download:

pip install pandas -i http://mirrors.aliyun.com/pypi/simple/   --trusted-host mirrors.aliyun.com
pip install pandas -i http://mirrors.aliyun.com/pypi/simple/

Aliyun: http://mirrors.aliyun.com/pypi/simple/
Douban: http://pypi.douban.com/simple/
Tsinghua University: https://pypi.tuna.tsinghua.edu.cn/simple/
University of Science and Technology of China: http://pypi.mirrors.ustc.edu.cn/simple/
```

## 3. Choosing the CUDA version

Choose the CUDA version, then add the following in `~/.zshrc`. If `nvcc -V` fails, you also need to add the following:

```shell
export CUDA_VER=version_number  # for example: 9.0

export PATH=/usr/local/cuda-$CUDA_VER/bin:$PATH

export LD_LIBRARY_PATH=/usr/local/cuda-$CUDA_VER/lib64:$LD_LIBRARY_PATH
```

The actual paths depend on where CUDA lives on your machine.

Finally, run `source ~/.zshrc` to apply.

CUDA version matching:

The major versions of PyTorch, the cudatoolkit, and the system CUDA need to match.

```shell
python -c "import torch; print(torch.version.cuda)"    # check PyTorch's CUDA version

conda list | grep cudatoolkit                          # check the cudatoolkit version

cat /path_to_cuda_your_using/version.txt               # check the system CUDA version. The path depends on ~/.zshrc.

# Or use: nvcc --version                                # check the system CUDA version
```

Note: even if those three match, if the GPU driver version does not match the CUDA version, CUDA will not work. Check whether CUDA is available:

```python
import torch
print(torch.cuda.is_available())
```

## 4. Passwordless server login

Use SSH keys. Copy the contents of the local `id_rsa.pub` file into `authorized_keys` in `.ssh/` on the target server. If the file does not exist, create it and `cat` the local `id_rsa.pub` into it.

If there are problems, the folder permissions may be wrong:
[https://serverfault.com/questions/525045/ssh-connection-asks-for-password-although-key-is-accepted](https://serverfault.com/questions/525045/ssh-connection-asks-for-password-although-key-is-accepted)

```shell
chmod 755 ~/.ssh                  # set the .ssh directory permissions to 755
```

Or it could be a copy error. The recommendation is to first rsync the local `id_rsa.pub` to the target machine, then run:

```shell
cat temp.pub >> authorized_keys
```
