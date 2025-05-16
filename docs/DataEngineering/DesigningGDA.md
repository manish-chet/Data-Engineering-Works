# Data Engineering and Architecture Overview

## Successful data engineering is built upon rock-solid data architecture

---

## What Is Data Architecture?

Enterprise architecture is the design of systems to support change in the enterprise, achieved by flexible and reversible decisions reached through careful evaluation of trade-offs.

### Data Architecture Defined

Data architecture is a subset of enterprise architecture, inheriting its properties: processes, strategy, change management, and evaluating trade-offs. Here are a couple of definitions of data architecture that influence our definition:

**TOGAF’s definition**  
TOGAF defines data architecture as follows:  
*A description of the structure and interaction of the enterprise’s major types and sources of data, logical data assets, physical data assets, and data management resources.*

**DAMA’s definition**  
*Identifying the data needs of the enterprise (regardless of structure) and designing and maintaining the master blueprints to meet those needs. Using master blueprints to guide data integration, control data assets, and align data investments with business strategy.*

**Our Definition**  
Data architecture is the design of systems to support the evolving data needs of an enterprise, achieved by flexible and reversible decisions reached through a careful evaluation of trade-offs.

---

### Operational vs Technical Architecture

- **Operational architecture** encompasses the functional requirements related to people, processes, and technology.
  - What business processes does the data serve?
  - How is data quality managed?
  - What is the latency from data production to availability?

- **Technical architecture** outlines how data is ingested, stored, transformed, and served.
  - For example, how will you move 10 TB of data every hour from a source database to your data lake?

> Operational architecture describes **what** needs to be done.  
> Technical architecture describes **how** it will happen.

---

## “Good” Data Architecture

> Never shoot for the best architecture, but rather the least worst architecture.  
> — *Mark Richards and Neal Ford*

Good data architecture is:
- Flexible and maintainable.
- Evolves with business and technology changes.
- Designed for reversibility to reduce cost of changes.

Bad data architecture is:
- Tightly coupled, rigid, overly centralized.
- Uses the wrong tools for the job.
- Hampers development and change management.

---

## Principles of Good Data Architecture

### AWS Well-Architected Framework (6 Pillars)
- Operational excellence
- Security
- Reliability
- Performance efficiency
- Cost optimization
- Sustainability

### Google Cloud’s Five Principles for Cloud-Native Architecture
- Design for automation.
- Be smart with state.
- Favor managed services.
- Practice defense in depth.
- Always be architecting.

### Principles of Data Engineering Architecture
1. Choose common components wisely  
2. Plan for failure  
3. Architect for scalability  
4. Architecture is leadership  
5. Always be architecting  
6. Build loosely coupled systems  
7. Make reversible decisions  
8. Prioritize security  
9. Embrace FinOps  

---

## Major Architecture Concepts

### Domains and Services

- A **domain** is the real-world subject area you’re architecting for.
- A **service** is a set of functionality designed to accomplish a task.

**Example:**
- *Sales Domain*: services = orders, invoicing, products.
- *Accounting Domain*: services = invoicing (shared), payroll, accounts receivable.

> Talk to users and stakeholders to determine what the domain should encompass and what services to include.  
> Avoid architecting in a vacuum.

---

### Distributed Systems, Scalability, and Designing for Failure

We focus on four characteristics:

- **Scalability**: Improve performance to handle demand.
- **Elasticity**: Dynamically scale up/down based on workload.
- **Availability**: Percentage of uptime.
- **Reliability**: Probability of successful function during a specific interval.

**Key Relationships:**
- Low reliability = low availability.
- Elasticity supports reliability.
- Distributed systems improve scaling and fault tolerance.

**Vertical vs Horizontal Scaling:**
- Vertical = one machine with more resources.
- Horizontal = multiple machines (preferred for resilience).

**Modern Distributed Architecture:**
- Leader node coordinates tasks.
- Worker nodes execute.
- Redundancy ensures continuity in case of failures.

Distributed systems are foundational in most modern cloud data technologies.

---




## Tight Versus Loose Coupling: Tiers, Monoliths, and Microservices

### Architecture Tiers

In a **single-tier architecture**, your database and application are tightly coupled, residing on a single server. This server could be your laptop or a single virtual machine (VM) in the cloud. The tightly coupled nature means if the server, database, or application fails, the entire architecture fails. While single-tier architectures are good for prototyping and development, they are not advised for production environments due to obvious failure risks.

### Multitier Architecture

A **multitier** architecture (also known as n-tier architecture) decouples data and application layers. These layers are hierarchical, where the lower layers are independent of the upper layers, but the upper layers depend on the lower ones. A common example is the **three-tier architecture**, which consists of:
- **Data** tier
- **Application logic** tier
- **Presentation** tier

Each tier is isolated, allowing for separation of concerns and flexibility in choosing technologies within each tier.

### Monoliths

A **monolith** is an architecture where as much functionality as possible is bundled into a single codebase running on a single machine. Monoliths are characterized by tight coupling, both technically (across architectural tiers) and domain-wise (in how domains are interwoven). The tight coupling within a monolith can make it difficult to swap out or upgrade components, often requiring extensive rewiring of other areas of the architecture. 

Because of this tight coupling, monolithic architectures lack modularity, making it hard to reuse components across the architecture and improve parts without unintended side effects.

### Microservices

In contrast, **microservices** architecture is based on separate, decentralized, and loosely coupled services. Each microservice performs a specific function and operates independently, meaning that if one service goes down, it doesn’t impact the others. Microservices offer greater flexibility, scalability, and fault tolerance compared to monolithic systems, making them ideal for large, complex applications that require frequent updates and scaling.

---

Considerations for Data Architecture

User Access: Single Versus Multitenant
As a data engineer, you have to make decisions about sharing systems across multiple teams, organizations, and customers. In some sense, all cloud services are multitenant, although this multitenancy occurs at various grains. For example, a cloud compute instance is usually on a shared server, but the VM itself provides some degree of isolation. Object storage is a multitenant system, but cloud vendors guarantee security and isolation so long as customers configure their permissions correctly.

Engineers frequently need to make decisions about multitenancy at a much smaller scale. For example, do multiple departments in a large company share the same data warehouse? Does the organization share data for multiple large customers within the same table?

We have two factors to consider in multitenancy: performance and security. With multiple large tenants within a cloud system, will the system support consistent performance for all tenants, or will there be a noisy neighbor problem? (That is, will high usage from one tenant degrade performance for other tenants?) Regarding security, data from different tenants must be properly isolated. When a company has multiple external customer tenants, these tenants should not be aware of one another, and engineers must prevent data leakage. Strategies for data isolation vary by system. For instance, it is often perfectly acceptable to use multitenant tables and isolate data through views. However, you must make certain that these views cannot leak data. Read vendor or project documentation to understand appropriate strategies and risks.

Event-Driven Architecture
Your business is rarely static. Things often happen in your business, such as getting a new customer, a new order from a customer, or an order for a product or service. These are all examples of events that are broadly defined as something that happened, typically a change in the state of something. For example, a new order might be created by a customer, or a customer might later make an update to this order.

An event-driven workflow (Figure 3-8) encompasses the ability to create, update, and asynchronously move events across various parts of the data engineering lifecycle. This workflow boils down to three main areas: event production, routing, and consumption. An event must be produced and routed to something that consumes it without tightly coupled dependencies among the producer, event router, and consumer.

Figure 3-8. In an event-driven workflow, an event is produced, routed, and then consumed.

An event-driven architecture (Figure 3-9) embraces the event-driven workflow and uses this to communicate across various services. The advantage of an event-driven architecture is that it distributes the state of an event across multiple services. This is helpful if a service goes offline, a node fails in a distributed system, or you’d like multiple consumers or services to access the same events. Anytime you have loosely coupled services, this is a candidate for event-driven architecture. Many of the examples we describe later in this chapter incorporate some form of event-driven architecture.

Brownfield Versus Greenfield Projects
Before you design your data architecture project, you need to know whether you’re starting with a clean slate or redesigning an existing architecture. Each type of project requires assessing trade-offs, albeit with different considerations and approaches. Projects roughly fall into two buckets: brownfield and greenfield.

Brownfield Projects
Brownfield projects often involve refactoring and reorganizing an existing architecture and are constrained by the choices of the present and past. Because a key part of architecture is change management, you must figure out a way around these limitations and design a path forward to achieve your new business and technical objectives. Brownfield projects require a thorough understanding of the legacy architecture and the interplay of various old and new technologies. All too often, it’s easy to criticize a prior team’s work and decisions, but it is far better to dig deep, ask questions, and understand why decisions were made. Empathy and context go a long way in helping you diagnose problems with the existing architecture, identify opportunities, and recognize pitfalls.

Greenfield Projects
On the opposite end of the spectrum, a greenfield project allows you to pioneer a fresh start, unconstrained by the history or legacy of a prior architecture. Greenfield projects tend to be easier than brownfield projects, and many data architects and engineers find them more fun! You have the opportunity to try the newest and coolest tools and architectural patterns. What could be more exciting?

You should watch out for some things before getting too carried away. We see teams get overly exuberant with shiny object syndrome. They feel compelled to reach for the latest and greatest technology fad without understanding how it will impact the value of the project. There’s also a temptation to do resume-driven development, stacking up impressive new technologies without prioritizing the project’s ultimate goals. Always prioritize requirements over building something cool.

Whether you’re working on a brownfield or greenfield project, always focus on the tenets of “good” data architecture. Assess trade-offs, make flexible and reversible decisions, and strive for positive ROI.


Examples and Types of Data Architecture
Data Warehouse
A data warehouse is a central data hub used for reporting and analysis. Data in a data warehouse is typically highly formatted and structured for analytics use cases. It’s one of the oldest and most well-established data architectures.

In the past, data warehouses were widely used by enterprises with significant budgets (often in the millions of dollars) to acquire data systems and support internal teams. This approach was expensive and labor-intensive. With the rise of cloud technologies, the scalable, pay-as-you-go model made cloud data warehouses accessible even to smaller companies. Since a third-party provider manages the data warehouse infrastructure, companies can do more with fewer people, even as their data complexity grows.

Types of Data Warehouse Architecture
Organizational Architecture: This organizes data according to business team structures and processes.

Technical Architecture: This reflects the technical nature of the data warehouse, such as Massively Parallel Processing (MPP).

Cloud Data Warehouse
Cloud data warehouses represent a significant evolution of the traditional on-premises data warehouse. Amazon Redshift kicked off the cloud data warehouse revolution by allowing companies to spin up a Redshift cluster on demand, scale it over time, and delete clusters when no longer needed. Other competitors, like Google BigQuery and Snowflake, popularized the idea of separating compute from storage.

With cloud data warehouses, data is housed in object storage, providing virtually limitless storage. Compute power can be spun up on demand, making big data capabilities available on an ad hoc basis without the long-term cost of maintaining thousands of nodes.

Cloud data warehouses can process petabytes of data in a single query and support data structures such as complex JSON documents, enabling them to handle use cases previously reserved for Hadoop clusters.

Data Marts
A data mart is a refined subset of a data warehouse designed to serve analytics and reporting needs for a specific department, suborganization, or line of business. For example, each department within a company might have its own data mart tailored to its needs.

Data marts serve two purposes:

Improved Data Access: They make data more easily accessible to analysts and report developers.

Performance Enhancement: They offer an additional transformation step beyond the initial ETL or ELT pipelines, improving performance for complex queries and joins, especially when the raw data is large.

Data Lake
The data lake is one of the most popular architectures that emerged during the big data era. Instead of imposing structural limitations on data, a data lake allows storing all data—structured and unstructured—in a central location. The first generation of data lakes, called "Data Lake 1.0," had its shortcomings but was a significant step forward.

Initially built on HDFS, data lakes moved to cloud-based object storage, offering extremely cheap storage with virtually limitless capacity. This architecture allows for the storage of immense amounts of data in any format, and on-demand compute power can be used to query or transform this data.

Despite its promises, Data Lake 1.0 had its challenges:

Data Management: Without schema management and proper cataloging tools, data lakes often became unmanageable.

Processing Issues: Data processing was difficult due to the lack of simple data manipulation tools like SQL for operations like deleting or updating records.

Cost and Complexity: Managing Hadoop clusters required significant resources, and the cost of building and maintaining these clusters ballooned due to the complexities involved.

Despite these challenges, many organizations—especially large tech companies like Netflix and Facebook—found significant value in data lakes, though smaller organizations struggled to realize the same benefits.







Convergence, Next-Generation Data Lakes, and the Data Platform
In response to the limitations of first-generation data lakes, various players have sought to enhance the concept to fully realize its promise. For example, Databricks introduced the notion of a data lakehouse. The lakehouse incorporates the controls, data management, and data structures found in a data warehouse while still housing data in object storage and supporting a variety of query and transformation engines. In particular, the data lakehouse supports atomicity, consistency, isolation, and durability (ACID) transactions—a big departure from the original data lake, where you simply pour in data and never update or delete it.

The term data lakehouse suggests a convergence between data lakes and data warehouses. The technical architecture of cloud data warehouses has evolved to be very similar to a data lake architecture. Cloud data warehouses:

Separate compute from storage

Support petabyte-scale queries

Store a variety of unstructured data and semi-structured objects

Integrate with advanced processing technologies such as Spark or Beam

We believe that the trend of convergence will only continue. The data lake and the data warehouse will still exist as different architectures. In practice, their capabilities will converge so that few users will notice a boundary between them in their day-to-day work.

We now see several vendors offering data platforms that combine data lake and data warehouse capabilities. From our perspective, AWS, Azure, Google Cloud, Snowflake, and Databricks are class leaders, each offering a constellation of tightly integrated tools for working with data, running the gamut from relational to completely unstructured.

Instead of choosing between a data lake or data warehouse architecture, future data engineers will have the option to choose a converged data platform based on a variety of factors, including:

Vendor

Ecosystem

Relative openness


Modern Data Stack
The modern data stack (Figure 3-13) is currently a trendy analytics architecture that highlights the type of abstraction we expect to see more widely used over the next several years. Whereas past data stacks relied on expensive, monolithic toolsets, the main objective of the modern data stack is to use cloud-based, plug-and-play, easy-to-use, off-the-shelf components to create a modular and cost-effective data architecture.

These components include:

Data pipelines

Storage

Transformation

Data management/governance

Monitoring

Visualization

Exploration

The domain is still in flux, and the specific tools are changing and evolving rapidly, but the core aim will remain the same: to reduce complexity and increase modularization. Note that the notion of a modern data stack integrates nicely with the converged data platform idea from the previous section.

Key Outcomes of the Modern Data Stack:
Self-service (analytics and pipelines)

Agile data management

Using open-source tools or simple proprietary tools with clear pricing structures

Community is a central aspect of the modern data stack as well. Unlike products of the past that had releases and roadmaps largely hidden from users, projects and companies operating in the modern data stack space typically have strong user bases and active communities. These communities participate in the development by:

Using the product early

Suggesting features

Submitting pull requests to improve the code



Lambda Architecture
In the "old days" (the early to mid-2010s), the popularity of working with streaming data exploded with the emergence of Kafka as a highly scalable message queue and frameworks such as Apache Storm and Samza for streaming/real-time analytics. These technologies allowed companies to perform new types of analytics and modeling on large amounts of data, such as:

User aggregation and ranking

Product recommendations

Data engineers needed to figure out how to reconcile batch and streaming data into a single architecture. The Lambda architecture was one of the early popular responses to this problem.

In a Lambda architecture (Figure 3-14), you have systems operating independently of each other—batch, streaming, and serving. The source system is ideally immutable and append-only, sending data to two destinations for processing: stream and batch.

Stream processing: This intends to serve the data with the lowest possible latency in a "speed" layer, usually a NoSQL database.

Batch processing: Data is processed and transformed in a system such as a data warehouse, creating precomputed and aggregated views of the data.

Serving layer: This provides a combined view by aggregating query results from the two layers.

Challenges of Lambda Architecture:
Managing multiple systems with different codebases is difficult and error-prone, creating systems where code and data are extremely difficult to reconcile.

While Lambda architecture still gets attention and remains popular in search-engine results for data architecture, it's no longer the recommended approach for combining streaming and batch data for analytics



Kappa Architecture
As a response to the shortcomings of Lambda architecture, Jay Kreps proposed an alternative called Kappa architecture (Figure 3-15). The central thesis of Kappa architecture is this: Why not just use a stream-processing platform as the backbone for all data handling—ingestion, storage, and serving? This facilitates a true event-based architecture. Real-time and batch processing can be applied seamlessly to the same data by:

Reading the live event stream directly

Replaying large chunks of data for batch processing

Key Points of Kappa Architecture:
Unified stream processing: Instead of managing separate systems for batch and real-time processing, everything is handled through a stream-processing platform.

Event-based: This architecture supports a truly event-driven design, where data is continuously processed as it flows in.

Though the original Kappa architecture article came out in 2014, it hasn’t been widely adopted. There may be a couple of reasons for this:

Complexity of streaming: Streaming is still a bit of a mystery for many companies; it’s easy to talk about, but harder than expected to execute.

Cost and complexity: Kappa architecture can be complicated and expensive in practice. While some streaming systems can scale to huge data volumes, they are complex and costly. Batch storage and processing remain much more efficient and cost-effective for enormous historical datasets.

Data Mesh
The data mesh is a recent response to sprawling monolithic data platforms, such as centralized data lakes and data warehouses, and "the great divide of data," where the landscape is divided between operational data and analytical data.

The data mesh attempts to invert the challenges of centralized data architecture by taking the concepts of domain-driven design (commonly used in software architectures) and applying them to data architecture.

Because the data mesh has captured much recent attention, you should be aware of it as an emerging approach in modern data architectures.


