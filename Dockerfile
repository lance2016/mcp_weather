FROM ubuntu:22.04

# 设置非交互式环境
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 安装基本工具和Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    curl \
    tzdata \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置Python别名
RUN ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip

WORKDIR /app

COPY requirements.txt .
COPY pyproject.toml .

# 安装需要的Python包和mcp-server-fetch
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install -e .

# 确保mcp-server-fetch可执行
RUN which mcp-server-fetch

# 修改app.py中的script_path配置
COPY . .
RUN sed -i 's|script_path="mcp-server-fetch"|script_path="/usr/local/bin/mcp-server-fetch"|g' app.py

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]