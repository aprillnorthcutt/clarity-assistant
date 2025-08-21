# 🧾 Clarity Assistant -- Audit & Financial AI Tools

> 🌐 Live App: <https://clarity-assistant.azurewebsites.net>\
> 🧠 NLP-Powered by: Azure OpenAI GPT-4o\
> 🧩 Part of: [AI Tools Hub](https://ai-tools-hub.azurewebsites.net/)

------------------------------------------------------------------------

## 📌 Overview

**Clarity Assistant** is a dual-purpose platform offering two distinct,
AI-powered solutions:

### 🔍 Audit Clarity Assistant

Helps nonprofit financial auditors review and revise audit notes for
clarity, specificity, and GAAP compliance. The assistant flags vague or
ambiguous language and suggests precise alternatives---particularly for
complex disclosures such as donated services, multi-year pledges, and
restricted grants.

### 💰 Financial Clarity Assistant

Designed for individuals who need help clarifying vague financial notes,
budgeting under new constraints, and generating actionable plans. This
tool analyzes loosely defined goals (e.g., "save money" or "figure out
debt") and delivers specific steps and re-analysis as conditions change.

> The **Audit Clarity Assistant** and **Financial Clarity Assistant**
> are two distinct NLP-driven tools, deployed under a shared application
> and powered by a unified Azure OpenAI GPT-4o backend.
>
> Though served through the same Streamlit interface, each assistant
> operates independently---driven by prompt engineering, YAML
> configuration (for audit), and branching logic (for financial tasks).
> This shared deployment highlights a modular, scalable approach to
> AI-powered domain solutions.

------------------------------------------------------------------------

## ✨ Features

-   ✅ **Streamlit UI** with dropdown-driven module selection (audit)
-   📄 **YAML Modules** defining audit-specific checks, guidance, and
    context
-   💬 GPT-4o **multi-turn prompt generation** (system + user roles)
-   🧠 Domain-specific modeling for nonprofit audits & personal finance
-   🔄 Clear before→after redlines and follow-up recommendations
-   ☁️ **Deployed to Azure Web App** for live interaction and feedback

------------------------------------------------------------------------

## ⚙️ Tech Stack

-   **Frontend**: Streamlit (Python)
-   **Backend AI**: Azure OpenAI (GPT-4o)
-   **Prompt Logic**: Modular YAML (Audit), In-line Conditionals
    (Financial)
-   **Hosting**: Azure Web App (Linux)
-   **CI/CD**: GitHub Actions (optional)
-   **Infrastructure**: Terraform (planned)

------------------------------------------------------------------------

## 💻 Developer Notes

-   All audit modules are stored in `modules/` as `module{n}.yaml`
    files.
-   Prompts are dynamically assembled using `prompt_builder.py`.
-   Module data is loaded via `module_loader.py`, with guard clauses for
    stability.
-   App routing uses Streamlit's `pages/` folder to isolate assistant
    logic.
-   🧠 Both assistants are backed by a **shared Azure OpenAI GPT-4o
    endpoint**, with behavior separated via targeted prompt construction
    and assistant-specific rules.

------------------------------------------------------------------------

## 👩‍💻 About the Developer

April Northcutt 
- **Software Engineering Manager | Backend Developer | Cloud & AI Enthusiast**  
📫 [LinkedIn](https://www.linkedin.com/in/aprilnorthcutt/) \| 🌐 [AI
Tools Hub](https://ai-tools-hub.azurewebsites.net/) \|
📂 GitHub: [github.com/aprillnorthcutt](https://github.com/aprillnorthcutt)  

- Certifications: *Azure Developer Associate, Azure Administrator Associate, Azure Fundamentals, AI Fundamentals, Microsoft 365 Fundamentals, Certified Scrum Developer (ASD), Green Software for Practitioners (LFC131), ICAgile Certified Professional (ICP)*  


## 📎 Future Enhancements

-   Add budget visualizations and historical goal tracking to Financial
    Assistant
-   Expand audit module YAMLs with GAAP citations and industry-specific
    logic
-   Terraform deployment and modular CI/CD
-   Persistent backend for action tracking

------------------------------------------------------------------------
