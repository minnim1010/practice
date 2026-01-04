# UV 사용법, 명령어 및 초기 세팅

## UV란 무엇인가?

UV는 Rust로 작성된 매우 빠른 Python 패키지 설치 및 해결 도구입니다. `pip` 및 `pip-tools`와 호환되면서도 훨씬 빠른 성능을 제공합니다.

## 설치

UV는 `curl`, `pip`, `brew` 등 다양한 방법으로 설치할 수 있습니다.

**macOS 및 Linux (curl):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**pip:**
```bash
pip install uv
```

**Homebrew (macOS):**
```bash
brew install uv
```

## 기본 명령어

### 가상 환경 생성

`uv venv` 명령어를 사용하여 가상 환경을 생성합니다.

```bash
uv venv
```

기본적으로 `.venv`라는 이름의 가상 환경이 생성됩니다. 다른 이름을 사용하려면 다음과 같이 지정합니다.

```bash
uv venv my-venv
```

Python 버전은 다음과 같이 지정합니다.

```bash
uv venv --python 3.13
```

### 가상 환경 활성화

**macOS 및 Linux:**
```bash
source .venv/bin/activate
```

### 패키지 설치

`uv pip install` 명령어를 사용하여 패키지를 설치합니다. `pip install`과 동일한 방식으로 사용할 수 있습니다.

```bash
uv pip install requests
```

`requirements.txt` 파일로부터 패키지를 설치할 수도 있습니다.

```bash
uv pip install -r requirements.txt
```

### 패키지 삭제

`uv pip uninstall` 명령어를 사용하여 패키지를 삭제합니다.

```bash
uv pip uninstall requests
```

## 가상 환경 관리

UV는 가상 환경 생성 및 관리를 위한 편리한 기능을 제공합니다.

- **가상 환경 생성:** `uv venv`
- **가상 환경 경로 확인:** `uv venv --path`
- **가상 환경 삭제:** `rm -rf .venv` (또는 해당 가상 환경 폴더)

## 의존성 관리

`uv pip compile` 및 `uv pip sync`를 사용하여 `pip-tools`와 유사하게 의존성을 관리할 수 있습니다.

### 의존성 파일 생성

`requirements.in` 파일에 직접 의존성을 명시합니다.

**requirements.in:**
```
fastapi
uvicorn
```

`uv pip compile` 명령어를 사용하여 `requirements.txt` 파일을 생성합니다.

```bash
uv pip compile requirements.in -o requirements.txt
```

### 의존성 동기화

`uv pip sync` 명령어를 사용하여 가상 환경의 패키지를 `requirements.txt` 파일과 동기화합니다. `requirements.txt`에 명시된 패키지만 설치되고, 명시되지 않은 패키지는 제거됩니다.

```bash
uv pip sync requirements.txt
```

### `pyproject.toml` 초기화

`uv init` 명령어를 사용하여 `pyproject.toml` 파일을 생성하고 프로젝트를 초기화할 수 있습니다. 이 명령어는 프로젝트 이름, 버전, 의존성 등을 대화형으로 설정할 수 있도록 도와줍니다.

```bash
uv init
```

## `pyproject.toml` 사용

UV는 `pyproject.toml` 파일을 사용하여 프로젝트의 의존성을 관리하는 것을 지원합니다. 이는 PEP 621 표준을 따르는 현대적인 Python 프로젝트 관리 방식입니다.

### `pyproject.toml`에 의존성 정의

`[project]` 테이블 아래에 `dependencies`와 `optional-dependencies`를 사용하여 의존성을 정의할 수 있습니다.

**pyproject.toml 예시:**
```toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = [
    "fastapi",
    "uvicorn",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "ruff",
]
```

### `pyproject.toml`에서 의존성 설치

`uv pip install` 명령어를 사용하여 `pyproject.toml`에 정의된 의존성을 설치할 수 있습니다.

현재 프로젝트를 편집 가능 모드로 설치하려면:
```bash
uv pip install -e .
```

개발용 의존성을 포함하여 설치하려면:
```bash
uv pip install -e '.[dev]'
```

### `pyproject.toml`과 동기화

`uv pip sync`를 사용하여 `pyproject.toml`의 의존성으로 가상 환경을 동기화할 수 있습니다. 이 명령어는 `pyproject.toml`에 명시된 패키지만을 가상 환경에 유지합니다.

```bash
uv pip sync --all-extras
```
