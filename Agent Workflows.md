# 워크플로우 개요

## 워크플로우란?

워크플로우는 여러 AI 에이전트를 조율하여 복잡한 작업을 단계적으로 수행하는 자동화 시스템입니다.

## 워크플로우 타입

```
# Microsoft Foundry - Workflow 는 유형별 템플릿을 제공합니다.

Single Agent → Sequential Workflow → Group Chat → Human-in-loop
(단순)                                                    (복잡)
```

| 타입 | 설명 | 사용 사례 |
|------|------|-----------|
| **Sequential** | 순차적 실행 | 데이터 파이프라인, 문서 처리 |
| **Group Chat** | 에이전트 간 대화 | 협업 문제 해결, 의사결정 |
| **Human-in-loop** | 사람 개입 | 승인 프로세스, 검증 |

## 워크플로우 구성 요소
    Workflow
     ├─ Template (Sequential / Human / Group)
     ├─ Nodes
     │   ├─ Agent Node
     │   ├─ Logic Node (If/Else, For Each, Go To)
     │   ├─ Data Transformation Node (데이터 처리 및 변수 관리)
     │   └─ User Interaction Node (메시지 보내기, 질문하기)
     ├─ Agents
     ├─ Execution Context
     └─ Run & Save

---

# 1. Sequential Workflow
  - 에이전트 및 노드가 정해진 순서대로 직렬 실행합니다.
  - 이전 단계의 출력이 다음 단계의 입력으로 전달됩니다.
  - 파이프라인, 단계별 처리에 적합합니다.

### 대표 시나리오
  - 문서 입력 -> 요약 -> 분류 -> 응답 생성
  - 티켓 처리 파이프라인
  - RGA 전처리 -> 응답 생성 -> 후처리


## New Foundry UI 로 전환
   - Microsoft Foundry Portal (https://ai.azure.com) 에서 우측 상단에 새 Foundry 토글을 활성화 하고, 이전 실습에서 만들어 놓은 프로젝트를 선택합니다.
    <img width="1992" height="1125" alt="image" src="https://github.com/user-attachments/assets/3c1b81d4-dc31-4f74-9daa-02c3edbc7721" />
   - 우측 상단에 빌드 메뉴를 클릭하면 왼편에 Foundry Build 메뉴들을 확인할 수 있습니다.
     이제 에이전트 및 워크플로우를 생성할 준비가 되었습니다.

## 필요한 에이전트 생성

먼저 워크플로우에서 사용할 에이전트들을 생성하기 위해 에이전트 만들기를 클릭합니다.

### TravelPlannerAgent

  - 에이전트 이름: TravelPlannerAgent
  - 모델 : gpt-5.2 (앞 실습에서 배포한 다른 GPT 모델을 선택할 수 있습니다.)
  - 지침 :
    ```
    당신은 여행 계획 전문가입니다.
    
    역할:
    1. 사용자의 여행 요구사항을 분석합니다
    2. 목적지의 주요 관광지, 맛집, 숙소를 추천합니다
    3. 일자별 여행 일정을 구체적으로 작성합니다
    4. 예상 비용과 준비물을 제시합니다
    
    출력 형식:
    - 목적지 개요
    - 일자별 일정 (아침/점심/저녁 활동)
    - 추천 숙소
    - 예상 비용
    - 준비물 목록
    
    다음 에이전트에게 넘길 정보: 전체 여행 계획
    ```
    <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/388da360-ecb6-4d21-bdda-4337c83d18c1" />
    
### LocalAgent

  - 에이전트 이름: LocalAgent
  - 모델 : gpt-5.2 (앞 실습에서 배포한 다른 GPT 모델을 선택할 수 있습니다.)
  - 지침 :
    ```
    당신은 현지 정보 전문가입니다.
    
    역할:
    1. 이전 에이전트의 여행 계획을 받습니다
    2. Web search를 사용하여 최신 현지 정보를 검색합니다
    3. 실시간 정보를 추가합니다:
       - 현재 날씨 및 기후
       - 현지 축제 및 이벤트
       - 교통 정보 (노선, 요금, 소요시간)
       - 영업시간 및 예약 정보
       - 현지 문화 및 주의사항
    
    출력 형식:
    - 원래 일정 + 현지 정보 보강
    - 교통편 상세 정보
    - 예약 필요 장소 목록
    - 현지 팁
    
    다음 에이전트에게 넘길 정보: 현지 정보가 추가된 여행 계획
    ```
   - **웹검색** 도구를 추가합니다.
     <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/a75e7b9c-3802-46e2-a9bc-ca5fc03df2e3" />

     <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/40ad45c1-3197-408e-b983-7b7a42d19f40" />
      
### TravelSummaryAgent

  - 에이전트 이름: TravelSummaryAgent
  - 모델 : gpt-5.2 (앞 실습에서 배포한 다른 GPT 모델을 선택할 수 있습니다.)
  - 지침 :
    ```
    당신은 여행 계획 정리 전문가입니다.
    
    역할:
    1. 이전 에이전트들의 정보를 종합합니다
    2. 실행 가능한 최종 계획으로 정리합니다
    3. 체크리스트를 생성합니다
    
    출력 형식:
    📋 여행 요약
    - 목적지: 
    - 기간:
    - 예산:
    
    📅 일정 요약 (한눈에 보는 일정)
    
    ✅ 출발 전 체크리스트
    - [ ] 항목1
    - [ ] 항목2
    
    🎒 준비물 체크리스트
    
    📞 긴급 연락처 및 유용한 정보
    
    최종 출력: 프린트 가능한 여행 가이드
    ```
    <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/ac6bafcf-ae85-499a-9fc0-5dfdc9794312" />
    <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/b2a296b8-aec6-48ed-a354-297995399e95" />

    
## Sequential Workflow 생성

**새 워크플로우 생성**

   - 워크플로우 > 만들기 > 순차 : **Sequential Workflow 템플릿**을 통해서 워크플로우를 생성합니다.
   
   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/0e0c193d-6c1f-48dc-ba07-6f30c34cd80a" />

**에이전트 추가**

   앞에서 만들어 놓은 에이전트를 순서대로 추가합니다.
   각 단계별 에이전트를 선택 -> 작업 ID 변경 -> 완료 로 진행합니다.

   - Step1
     - 작업 ID : TrevelPlanner
     - 에이전트 선택 : TravelPlannerAgent
   - Step2
     - 작업 ID : LocalSearch
     - 에이전트 선택 : LocalAgent
   - Step3
     - 작업 ID : TrevelSummary
     - 에이전트 선택 : TravelSummaryAgent
   
   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/85716da4-ea7f-4ace-9079-941834d8e3cd" />


**워크플로우 저장**

   - **저장** 버튼을 클릭합니다.
   - 워크플로우 이름 : Sequencial-TravelPlan

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/8eb61936-2fbc-44bf-b1fc-5884a73099cd" />


## 워크플로우 테스트

**미리보기 모드**

   - **미리보기** 버튼을 클릭합니다.
   - 여행 계획을 세워줄 것을 요청합니다.

**테스트 질문**

   ```
   제주도 2박 3일 여행 계획을 세워줘
   ```
   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/6eb27906-7536-40d1-a14b-00b0c1e9fb28" />


**실행 과정 관찰**

   각 단계에서의 출력을 확인합니다:

   - **Step 1 (TravelPlannerAgent)**: 기본 여행 일정 생성
   - **Step 2 (LocalAgent)**: 현지 정보 추가 (날씨, 교통, 이벤트)
   - **Step 3 (TravelSummaryAgent)**: 최종 요약 및 체크리스트

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/e8f3a92c-847a-4bd0-83ae-d325e3507d90" />
   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/cc208cb0-94df-4806-9e91-ff22c3285f70" />
   

**Traces 확인**

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/e8036a3c-6406-4159-8aa5-77d31f524607" />

   - 각 에이전트의 실행 시간
   - 에이전트 간 데이터 전달
   - 최종 출력 생성 과정

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/dcf47012-3dd6-4e8a-bd9d-e74dfda4e8d9" />

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/638526e4-32f3-4fac-a3bd-e6c30a476ab6" />

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/8e4e6d56-b40f-4208-a11e-54669909f272" />

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/7470f051-ef1e-4a14-bff5-a9e74c001d2c" />
   

## 워크플로우 배포 및 호출

**Publish**

   - **개시** 버튼을 클릭합니다.

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/93f7d7a4-0df3-41e0-98e0-c7f0cdd327d4" />

   - 워크플로우의 이름과 버전을 확인하고 게시합니다.

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/8a29c46c-fe6e-48bd-8d54-cb69b9ebe16f" />


**Python SDK로 호출**

   - [invokeworkflow.py](https://github.com/soondukkim/MicrosoftFoundry-AgentWorkflow/blob/main/invokeworkflow.py) 파일을 다운 받고, Visual Studio Code 에서 파일을 오픈합니다.
   - Code 에서 `PROJECT_ENDPOINT`, `WORKFLOW_NAME`, `WORKFLOW_VERSION` 값을 본인 환경에 맞게 수정합니다.
   - PROJECT_ENDPOINT 는 Foundry Portal 홈 화면에서 확인할 수 있습니다.
     <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/bbbb6ba1-f49d-4f61-9040-f93fb67cb9d0" />

   - 터미널에서 python invokeworkflow.py 를 실행합니다.

   > 💡 **실습 팁**: 아래 코드는 참고용입니다. 실제 실습 시에는 이 저장소의 루트 경로에 있는 `invokeWorkflow.py` 파일을 열어 `PROJECT_ENDPOINT`, `WORKFLOW_NAME`, `WORKFLOW_VERSION` 값을 본인 환경에 맞게 수정한 후 실행하세요.

   `invokeWorkflow.py` 파일 예시:
   ```python
   # Microsoft Foundry Workflow Invocation using Foundry SDK
   # Before running: pip install --pre azure-ai-projects>=2.0.0b1
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient
   from azure.ai.projects.models import ResponseStreamEventType
   
   # Project configuration
   PROJECT_ENDPOINT = "https://<foundry-resource-name>.services.ai.azure.com/api/projects/proj-default"
   WORKFLOW_NAME = "Sequential-Workflow"
   WORKFLOW_VERSION = "1"  # 게시된 버전으로 업데이트
   
   # Create AI Project client
   project_client = AIProjectClient(
       endpoint=PROJECT_ENDPOINT,
       credential=DefaultAzureCredential(),
   )
   
   with project_client:
       workflow = {
           "name": WORKFLOW_NAME,
           "version": WORKFLOW_VERSION,
       }
       
       # Get OpenAI client from project
       openai_client = project_client.get_openai_client()
   
       # Create a conversation
       conversation = openai_client.conversations.create()
       print(f"Created conversation (id: {conversation.id})")
   
       # Call the workflow with streaming
       print(f"\nCalling workflow: {WORKFLOW_NAME}...\n")
       stream = openai_client.responses.create(
           conversation=conversation.id,
           extra_body={"agent": {"name": workflow["name"], "type": "agent_reference"}},
           input="제주도 2박 3일 여행 일정 짜줘",
           stream=True,
           metadata={"x-ms-debug-mode-enabled": "1"},
       )
   
       # Process streaming events
       for event in stream:
           if event.type == ResponseStreamEventType.RESPONSE_OUTPUT_TEXT_DONE:
               print("\t", event.text)
           elif event.type == ResponseStreamEventType.RESPONSE_OUTPUT_ITEM_ADDED and event.item.type == "workflow_action":
               print(f"\n{'='*60}")
               print(f"Actor - '{event.item.action_id}':")
               print(f"{'='*60}")
           elif event.type == ResponseStreamEventType.RESPONSE_OUTPUT_ITEM_DONE and event.item.type == "workflow_action":
               print(f"\n✓ Workflow Item '{event.item.action_id}' is '{event.item.status}'")
               print(f"  (previous item was: '{event.item.previous_action_id}')")
           elif event.type == ResponseStreamEventType.RESPONSE_OUTPUT_TEXT_DELTA:
               print(event.delta, end="", flush=True)
   
       # Clean up
       print("\n\n✅ Workflow completed!")
       openai_client.conversations.delete(conversation_id=conversation.id)
       print("Conversation deleted")
   ```

**실행**

   ```bash
   pip install --pre azure-ai-projects>=2.0.0b1
   python invokeWorkflow.py
   ```

## ✅ 확인 사항

- 모든 에이전트가 순서대로 실행되는지 확인
- 각 에이전트의 출력이 다음 에이전트에 전달되는지 확인
- 최종 출력이 올바르게 생성되는지 확인

<img width="1772" height="1125" alt="image" src="https://github.com/user-attachments/assets/525f0d62-41a0-4969-87eb-73e621e58954" />

<img width="1772" height="1125" alt="image" src="https://github.com/user-attachments/assets/1c17a884-6313-4c8a-bc51-7ccab1de86f7" />

<img width="1772" height="1125" alt="image" src="https://github.com/user-attachments/assets/31e551d4-f8a4-46f8-9940-7f5379f14118" />


---

# 2. Group Chat Workflow
  - 여러 에이전트가 대화를 통해 협업하여 문제를 해결하는 워크플로우입니다.
  - 여러 에이전트가 컨텍스트/풀에 따라 제어권을 주고 받음
  - Fixed pipeline 이 아니라 동적 라우팅

### 대표 시나리오
  - Expert agent 핸드 오프
  - Excalation / Fallback 구조
  - Specialized agent 협업 (Student <-> Teacher)

## 필요한 에이전트 생성

먼저 워크플로우에서 사용할 에이전트들을 생성하기 위해 에이전트 만들기를 클릭합니다.

### StudentAgent

  - 에이전트 이름: StudentAgent
  - 모델 : gpt-5.2 (앞 실습에서 배포한 다른 GPT 모델을 선택할 수 있습니다.)
  - 지침 :
    ```
    너는 문제에 대답하는 에이전트야. 질문이 오면, 항상 답변해줘.
    
    역할:
    1. 사용자의 질문을 이해하고 답변을 생성합니다
    2. 첫 번째 시도에서는 기본적인 답변을 제공합니다
    3. TeacherAgent의 피드백을 받아 답변을 개선합니다
    4. 모든 요구사항이 충족될 때까지 답변을 수정합니다
    
    답변 시 고려사항:
    - 일정 (날짜, 시간)
    - 비용 (예산, 가격)
    - 취향 (선호도, 스타일)
    - 제약사항 (제한사항, 조건)
    
    개선이 필요하면 TeacherAgent의 피드백을 반영하여 답변을 보완합니다.
    ```
    <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/ebb83190-7c10-404d-9211-5e5d7ef6ddc7" />

### 2. TeacherAgent

  - 에이전트 이름: TeacherAgent
  - 모델 : gpt-5.2 (앞 실습에서 배포한 다른 GPT 모델을 선택할 수 있습니다.)
  - 지침 :
    ```
    너는 답변을 평가하는 에이전트야. 답변이 일정, 비용, 취향 등 다양한 조건에 대한 고려를 했다면 [COMPLETE]이라고 대답해줘. 아니라면, COMPLETE을 표시하지 말고, 수정을 요청해줘.
    
    평가 기준:
    1. 일정: 구체적인 날짜, 시간, 기간이 포함되었는가?
    2. 비용: 예산, 가격, 비용 정보가 포함되었는가?
    3. 취향: 사용자의 선호도나 스타일을 고려했는가?
    4. 실용성: 실제로 실행 가능한 계획인가?
    5. 완성도: 모든 필요한 정보가 포함되었는가?
    
    응답 형식:
    평가 완료 시: "[COMPLETE] 모든 조건이 충족되었습니다."
    개선 필요 시: "다음 사항을 보완해주세요: [구체적인 피드백]"
    
    중요: [COMPLETE]는 모든 기준이 충족되었을 때만 사용합니다.
    ```
    <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/f85c2419-657e-44e1-ac7e-d8e097305a2b" />

    <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/6767906f-87ca-4292-b1a0-9417a3f4995f" />



## Group Chat Workflow 생성

**새 워크플로우 생성**

   - 워크플로우 > 만들기 > 그룹 채팅 : **Group Chat Workflow 템플릿**을 통해서 워크플로우를 생성합니다.


**에이전트 추가**

   앞에서 만들어 놓은 에이전트를 순서대로 추가합니다.
   각 단계별 에이전트를 선택 -> 작업 ID 변경 -> 완료 로 진행합니다.

   - 에이전트 호출1
     - 작업 ID : student_agent
     - 에이전트 선택 : StudentAgent
   - 에이전트 호출2
     - 작업 ID : teacher_agent
     - 에이전트 선택 : TeacherAgent
   
   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/2262226e-a20c-403c-abf6-a7426885ae35" />


**대화 흐름 설정**

   ```
   User → StudentAgent → TeacherAgent → StudentAgent → ...
   ```
   - StudentAgent가 먼저 답변을 제공
   - TeacherAgent가 평가 및 피드백
   - [COMPLETE]가 나올 때까지 반복
   - 4회 대화 턴이 지나면 대화 종료

       If/Else 조건 확인 : 메시지에 'COMPLETE' 가 포함되어 있으면 종료
       - 만약
         ```
         !IsBlank(Find("[COMPLETE]", Upper(Last(Local.LatestMessage).Text)))
         ```
         <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/9657a96b-bab8-4fd2-83ea-ed6df9a2d380" />
    
       - 다음 조건 제외 : 최대 4회까지 대화가 이어지면 메시지를 보내기
         ```
         Local.TurnCount >= 4
         ```
         <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/0ed7484f-65d6-4041-9bd2-f6c100b12989" />
    
       - 그외 : Student 와 Teacher 대화 반복
     

**워크플로우 저장**

   - **저장** 버튼을 클릭합니다.
   - 워크플로우 이름 : GroupChat

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/c471c531-612a-46ea-b514-220442385336" />


## 워크플로우 테스트

**미리보기 모드**

   - **미리보기** 버튼을 클릭합니다.
   - 여행 계획을 세워줄 것을 요청합니다.

**테스트 질문**

   ```
   시애틀 2박 3일 여행 계획을 세워줘
   ```
   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/1b76f095-a656-4a89-b24b-a4a29eddfeaa" />
   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/b7f8c103-36b0-4c17-9639-3f55884101bf" />

**실행 과정 관찰**

   각 단계에서의 출력을 확인합니다:

   - **StudentAgent**: 문의에 맞는 답변 생성
   - **TeacherAgent**: StudentAgent 답변에 대한 피드백
   - **대화 종료 조건**: 대화 내용에 Complet 이 있거나 StudentAgent-TeacherAgent 간에 대화가 4회 반복되었는지 확인

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/e8f3a92c-847a-4bd0-83ae-d325e3507d90" />
   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/cc208cb0-94df-4806-9e91-ff22c3285f70" />
   

**Traces 확인**

   - **디버그** 버튼을 클릭합니다.
   - 워크플로우 단계별 실행 상세 내용을 확인합니다.
       - 각 에이전트의 실행 시간
       - 에이전트 간 데이터 전달
       - 최종 출력 생성 과정

   <img width="2000" height="1125" alt="image" src="https://github.com/user-attachments/assets/11d4dbc2-9d09-4aba-87c8-c69ac2eeb750" />


## 💡 Group Chat 활용 팁

- **역할 분담**: 각 에이전트에 명확한 역할 부여
- **종료 조건**: 무한 루프를 방지하기 위한 명확한 종료 조건
- **최대 턴 수**: 안전장치로 최대 턴 수 설정
- **피드백 구체성**: TeacherAgent의 피드백이 구체적일수록 개선 효과 증가

## ✅ 확인 사항

- 에이전트 간 대화가 자연스럽게 이어지는지 확인
- TeacherAgent의 평가 기준이 적절한지 확인
- [COMPLETE] 조건에서 워크플로우가 종료되는지 확인

---

# 3. Human-in-loop Workflow
  - 사람의 승인이나 입력이 필요한 지점에서 워크플로우를 일시 중지하는 패턴입니다.
  - Workflow 실행 중 사용자 입력을 기다렸다가 재개
  - 승인, 확인, 추가 정보 수집 용도

### 대표 시나리오
  - AI 결과에 대한 승인 프로세스
  - 계약, 보고서, 정책 문서 검토
  - 신뢰도 부족 시 사람에게 에스컬레이션


## Human-in-loop Workflow 시나리오
  - Human-in-Loop-workflow 템플릿과 앞의 Sequence Workflow 에서 만든 TravelPlannerAgent 를 기반으로 합니다:
  - [사용자 문의] -> TravelPlannerAgent -> [사용자 추가 문의] -> TravelPlannerAgent -> [사용자 종료]

### Human-in-Loop Workflow 생성

- **새 워크플로우 생성**
   - 워크플로우 -> 만들기
   - **Human-in-Loop Workflow** 템플릿을 선택합니다.
   <img width="1688" height="1125" alt="image" src="https://github.com/user-attachments/assets/59e378a5-c245-4f56-906f-add0c135dfa1" />

- **에이전트 추가**

   - 변수 설정 뒤에 + 아이콘을 클릭하여 에이전트 호출을 추가하고, TravelPlannerAgent 를 선택하고 작업 ID 를 'TrevelPlanner' 로 변경합니다:

   <img width="1688" height="1125" alt="image" src="https://github.com/user-attachments/assets/bb905a78-52ba-4a86-b8f3-dceb810d13dd" />

   <img width="1688" height="1125" alt="image" src="https://github.com/user-attachments/assets/5d8ac955-5446-4122-b882-f0fce9b2efd9" />

- **사람 개입 조건 변경**

   - 질문하기 노드에서 Ask a question 을 변경 후 완료 버튼을 클릭합니다.
   ```
   여행 계획에 만족하시나요? 만족하신다면 YES 를 입력해 주세요.
   ```
   <img width="1688" height="1125" alt="image" src="https://github.com/user-attachments/assets/1159cf4f-9307-46a6-b516-bbf39ce5ddf0" />

   If/Eles 조건의 'If' 노드의 조건 입력 후 완료 버튼을 클릭합니다.
   ```
   Local.ConfirmedInput <> "YES"
   ```
   <img width="1688" height="1125" alt="image" src="https://github.com/user-attachments/assets/7ca9a26f-dc18-4bd0-b1fa-d6b504da0f66" />

   다음으로 이동 노드의 Select action 에서 '에이전트 호출 : TravelPlanner' 선택 후 완료 버튼을 클릭합니다.

- **종료 메시지 변경**

   - If 뒤의 메시지보내기 노드를 삭제합니다.
   - <img width="1688" height="1125" alt="image" src="https://github.com/user-attachments/assets/ac283ef2-334e-4ec3-a089-d8521b1d42d0" />

   - Else 뒤의 메시지보내기 노드의 메시지를 수정합니다.
     
   ```
   Travel Agency 를 이용해 주셔서 감사합니다.
   ```
   
- **워크플로우 저장**
- 
   저장 버튼을 클릭하고 'Human-in-Loop' 로 저장합니다.


### 워크플로우 테스트

- **Preview 모드**

   - **미리보기** 버튼을 클릭합니다.

- **사용자 질문**

   ```
   시카고 2박 3일 여행 계획 세워줘.
   ```
   - TravelPlannerAgent 의 답변을 확인합니다.
   - 여행 시기에 맞는 추가 정보를 요청합니다.
   ```
   1월 날씨를 감안해서 준비할 것도 알려줘
   ```
   - 시카고의 1월 날씨에 맞는 여행 계획을 확인합니다.
   <img width="1688" height="1125" alt="image" src="https://github.com/user-attachments/assets/240919a6-c121-4a45-854d-e52c049c567e" />

   - 대화를 종료합니다.
   ```
   YES
   ```
   <img width="1688" height="1125" alt="image" src="https://github.com/user-attachments/assets/f7e41dd4-78a7-46a5-95cc-c6e96db6ee9d" />


- **실행 과정 관찰**

   각 단계에서의 출력을 확인합니다:

   - **Step 1 :** 기본 여행 계획 생성
   - **Step 2 :** 추가 문의에 대한 답변 내용
   - **Step 3 :** 사용자의 종료의사에 따른 대화 종료


## 💡 Human-in-loop 모범 사례

```
✅ 권장사항:
- 승인 지점을 명확히 표시
- 타임아웃 설정으로 무한 대기 방지
- 사용자에게 컨텍스트 제공 (이전 대화 요약)
- 간단한 승인 옵션 제공 (예/아니오/수정)

❌ 피해야 할 것:
- 너무 많은 승인 지점
- 불명확한 승인 질문
- 긴 타임아웃 (사용자 경험 저하)
- 승인 후 되돌리기 불가능한 구조
```

## ✅ 확인 사항

- 승인 지점에서 워크플로우가 올바르게 멈추는지 확인
- 승인/거부에 따라 적절히 분기되는지 확인
- 타임아웃이 정상 작동하는지 확인

---

# 📚 추가 리소스

- [Microsoft Foundry Workflows 개요](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/workflow?view=foundry)
- [Microsoft Agent Framework Workflows Orchestrations 패턴](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/overview)
