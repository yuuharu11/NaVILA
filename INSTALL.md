### 0. エイリアスの設定
python3とpythonのエイリアス
```bash
echo "alias python='python3'" >> ~/.zshrc
~/.zshrc
```

### 1. Miniconda のインストール

```bash
apt install wget
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -p $HOME/miniconda3
$HOME/miniconda3/bin/conda init bash
source $HOME/.bashrc && conda --version
```

### 2. 仮想環境の用意
まずは利用規約に同意
```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```
基本的なセットアップを行う
```bash
./environment_setup.sh navila
conda activate navila
# pyproject.tomlから必要なモジュールをダウンロード
/root/miniconda3/envs/navila/bin/python -m pip install -e .
```

### 3. 学習用データのダウンロード
```bash
hf download a8cheng/NaVILA-Dataset --repo-type dataset --local-dir /work/NaVILA-Dataset
```
次にYouTubeから動画のダウンロードを行う
```bash
pip install yt-dlp # 動画ダウンロード用のモジュール
yt-dlp -a video_ids.txt -o "/work/NaVILA-Dataset/Human/videos/%(id)s.%(ext)s"
```

ダウンロードしたp4ファイルをフレーム処理する。
```bash
apt-get update
apt-get install -y ffmpeg
python scripts/extract_rawframes.py
```

### 3'. 事前学習モデルのダウンロード（これは不要）
NaVILA向けの学習済みモデルはすでにhugging face上で提供されている。なお、GPUサーバー上の/ST2007O/datasets/huggingface/navila-llama3-8b-8fに保存してある。
```bash
hf download a8cheng/navila-llama3-8b-8f --repo-type model --local-dir /data/huggingface/navila-llama3-8b-8f
```

### 4. 学習
モジュールを用意する。
```bash
pip install transformers hydra-core omegaconf peft wandb opencv-python loguru datasets
# s2wrapperのダウンロード
/root/miniconda3/envs/navila/bin/python -m pip install git+https://github.com/bfshi/scaling_on_scales.git
# flash_attmのダウンロード
/root/miniconda3/envs/navila/bin/python -m pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.5.8/flash_attn-2.5.8+cu122torch2.3cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
 ./scripts/train/sft_8frames.sh 
```



