# Data Engineering Wiki

Welcome to the **Data Engineering Wiki** – a knowledge base built on book named **Fundamentals of DataEngineering** to help you understand the core concepts, lifecycle, and practical evolution of data engineering in modern data-driven systems.

---
## What is Data Engineering?
Data engineering is the development, implementation, and maintenance of systems and processes that take in raw data and produce high-quality, consistent information that supports downstream use cases, such as analysis and machine learning. Data engi‐neering is the intersection of security, data management, DataOps, data architecture, orchestration, and software engineering. A data engineer manages the data engineering lifecycle, beginning with getting data from source systems and ending with serving data for use cases, such as analysis or machine learning. 

A data engineer **gets data, stores it, and prepares it for consumption** by data scientists, analysts.
> — *Fundamentals of Data Engineering (O’Reilly)*
---
## Why Data Engineering?
Data Engineering acts as the foundation of the **modern data stack**, enabling:

- High-quality, accessible, and reliable data.
- Operational and analytical use cases across teams.
- Faster, scalable decision-making.

---
## Evolution of Data Engineering

- **1980s – Early 2000s**:"Data Warehousing to the Web" Focus on **ETL Developers**, **BI Engineers**, **Data Warehousing**.
The roots of the data engineer arguably lie in **data warehousing**, dating back to the 1970s and taking shape in the 1980s. With the development of the relational database and SQL, and their popularization by companies like Oracle, businesses needed tools and pipelines for reporting and business intelligence. Roles like BI engineer, ETL developer, and data warehouse engineer emerged to address these needs. Data warehouse and BI engineering are precursors to today's data engineering and still play a central role. The internet going mainstream in the mid-1990s created web-first companies and increased activity in supporting backend systems, which were often expensive and monolithic.
- **2006 – 2012**:" Birth of Contemporary Data Engineering" Hadoop ecosystem revolutionizes large-scale data processing.
After the dot-com bust, some survivors like Yahoo, Google, and Amazon became tech powerhouses. They initially relied on traditional systems but needed updated approaches to handle exploding data growth. These new systems needed to be **cost-effective, scalable, available, and reliable**. Coinciding with this, commodity hardware became cheap and ubiquitous, enabling innovations in distributed computation and storage on massive clusters. This ushered in the **"big data" era**. Big data is defined as extremely large datasets analyzed computationally to reveal patterns . A famous description uses the **three Vs: velocity, variety, and volume**. Google's publications on the Google File System (2003) and MapReduce (2004) were a "big bang" for data technologies and the cultural roots of modern data engineering [19]. Inspired by Google, Yahoo developed and open-sourced Apache Hadoop in 2006. This drew software engineers to large-scale data problems, leading to the birth of the **big data engineer** as data grew into terabytes and petabytes. Around the same time, Amazon created services like EC2, S3, and DynamoDB, offered as Amazon Web Services (AWS), becoming the first popular public cloud. The public cloud allowed developers to rent compute and storage instead of buying hardware, becoming a significant innovation. These early big data tools and the public cloud laid the foundation for today's data ecosystem.
- **2012 – Present**: Real-time processing, cloud-native stacks, streaming-first architecture.
---

## Key Concepts

- **Data Pipeline**: A series of processes to move data from source to destination.
- **ETL vs ELT**: Order of transformation matters depending on architecture.
- **Batch vs Streaming**: Batch handles large volumes at intervals, Streaming is real-time.
- **DataOps**: DevOps principles applied to data workflows.
- **Data Contracts**: Schema and quality guarantees between teams.
---

_“Data engineering is not about tools—it's about **building systems** that let others derive value from data.”_
