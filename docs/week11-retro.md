## Week11

## 1. 지금까지 구축한 개인 프로젝트를 Docker 컨테이너로 패키징하고 Docker Compose로 실행해보세요.

### Steps
#### Step 1 : Docker Image 생성
> 맥 os 환경 : 개인 프로젝트 폴더
1. Dockerfile 작성
```
FROM python:3.14-slim

# uv 바이너리 가져오기
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# 의존성 정의 파일만 먼저 복사 (레이어 캐시 최적화)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# 나머지 소스 코드 전체 복사 (src/, main.py, test.py 등)
COPY . .

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
2. .dockerignore 작성
3. `docker build -t chatbot-project`  
`docker build --platform linux/amd64 -t chatbot-project`  
EC2 인스턴스가 amd64이기 때문에 맞춰줘야 한다.

#### Step 2 : 만든 이미지를 Docker Compose로 실행
> 맥 os 환경 : 개인 프로젝트 폴더
1. docker-compose.yml 작성
```
services:
  chatbot-project:
    build: .
    image: chatbot-project
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./chroma_db:/app/chroma_db
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
    extra_hosts:
      - "host.docker.internal:host-gateway"  # Linux에서 필요
```
2. docker compose up 실행 시 서버 시동까지 자동으로 됨.

### 실행 결과
정상적으로 작동함을 확인. 

### Trouble Shooting
#### 문제 상황 1
올라마 사용시 주소 설정을 바꿔줘야한다.
```
services:
  chatbot-project:
    build: .
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
    extra_hosts:
      - "host.docker.internal:host-gateway"  # Linux에서 필요
```

#### 문제 상황 2
도커 이미지 파일이 너무 크다 9.2GB
```
docker run --rm -it chatbot-project sh -c "du -sh /app/.venv/lib/python3.14/site-packages/* 2>/dev/null | sort -rh | head -15"
2.9G	/app/.venv/lib/python3.14/site-packages/nvidia
```
-> linux/amd64 로 빌드하니까 왜 3.2GB 됐지...
-> 아까도 도커 허브에 올렸을때는 3.xGB 였던것같은데.
-> 그래도 크다


## 2. 개인 프로젝트의 컨테이너 이미지를 AWS EC2에 배포하고 외부에서 접근 가능하도록 구성해보세요.
### Steps
#### Step 1 : Docker Image를 Docer Hub에 올린다.
> 맥 os 환경
1. 도커 허브 로그인 `docker login -u <username>`
2. 이미지에 태그 달기 `docker tag chatbot-project:latest <username>/chatbot-project:latest`
3. `docker push <username>/chatbot-project:latest`

#### Step 2 : AWS EC2에서 도커 이미지를 받아 실행한다.
> EC2 환경
1. 프로젝트 폴더 생성 `mkdir chatbot-docker`, `cd chatbot-docker`
2. docker-compose.yml 작성
```
services:
  chatbot-project:
    image: <username>/chatbot-project:latest   # build 대신 image만 사용
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./chroma_db:/app/chroma_db
```
3. .env 작성  
EC2에서 Ollama 사용하려면 다시 설치해야하므로 gemini로 테스트
4. `docker compose up`

### 실행 결과

## 3. Github Actions를 활용해 코드 푸시 시 자동으로 개인 프로젝트가 빌드, 배포되는 CI/CD 파이프라인을 구축해보세요.


## (선택) 빅뱅 배포