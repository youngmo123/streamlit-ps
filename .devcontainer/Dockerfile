FROM mcr.microsoft.com/devcontainers/anaconda:1-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# Jupyter Notebook 설치 (선택사항)
RUN conda install -y jupyter

# Git 설치
RUN apt-get update && apt-get install -y git

# 한글 폰트 설치
RUN apt-get update && apt-get install -y fonts-nanum

# 한글 폰트 설정
RUN fc-cache -fv

# 음성파일 처리 ffmpeg 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg

# requirements.txt 파일을 컨테이너에 복사
COPY requirements.txt /workspace/requirements.txt

# requirements.txt 설치
RUN pip install -r /workspace/requirements.txt


