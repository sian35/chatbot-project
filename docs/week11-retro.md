## Week11

### 1. 지금까지 구축한 개인 프로젝트를 Docker 컨테이너로 패키징하고 Docker Compose로 실행해보세요.

#### 문제 상황 1
linux/arm64 로 설정되기 때문에 이미지 빌드할때 --platform linux/amd64 설정 필요

#### 문제 상황 2
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

#### 문제 상황 3
도커 이미지 파일이 너무 크다 9.2GB
```
docker run --rm -it chatbot-project sh -c "du -sh /app/.venv/lib/python3.14/site-packages/* 2>/dev/null | sort -rh | head -15"
2.9G	/app/.venv/lib/python3.14/site-packages/nvidia
```
-> linux/amd64 로 빌드하니까 왜 3.2GB 됐지...
-> 아까도 도커 허브에 올렸을때는 3.xGB 였던것같은데.
-> 그래도 크다


### 2. 개인 프로젝트의 컨테이너 이미지를 AWS EC2에 배포하고 외부에서 접근 가능하도록 구성해보세요.


### 3. Github Actions를 활용해 코드 푸시 시 자동으로 개인 프로젝트가 빌드, 배포되는 CI/CD 파이프라인을 구축해보세요.