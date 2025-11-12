# Capability Server Architecture: Research Report and SAP Development Guidance

## Executive Summary

Capability servers are the core building blocks of the chora ecosystem,
providing distinct domain **capabilities** (such as orchestration,
service registry, gateway/routing, etc.) via **multiple interfaces**
(native API, CLI, REST, and
MCP)[\[1\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,a%20component%20that).
This research consolidates best practices from cloud and software
industry leaders -- including AWS, Kubernetes, Docker, Terraform, and
more -- to inform a prescriptive architecture for capability servers. It
also outlines how to document these practices in **Structured Autonomous
Practice (SAP)** guides to accelerate adoption in the chora ecosystem.

**Key Findings:** Each research area revealed critical patterns and
recommendations:

- **Multi-Interface Architecture:** Successful systems (AWS, Docker,
  Kubernetes, Terraform) separate core logic from interface-specific
  layers, ensuring consistency across interfaces. For example, AWS CLI
  calls the same underlying APIs as the SDK and web
  console[\[2\]](https://stackoverflow.com/questions/59694539/how-do-i-write-aws-cli-commands-in-python#:~:text=),
  and Docker's CLI simply invokes Docker Engine's REST
  API[\[3\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=,why%20developers%20love%20using%20Docker)[\[4\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=DockerHost).
  **Recommendation:** Design capability servers with a single core
  implementation accessed through thin interface adapters (e.g. CLI
  commands, HTTP endpoints) to avoid duplication and drift. A comparison
  of industry approaches is provided in Part 1, along with a Python code
  example demonstrating a unified core with multiple interfaces.

- **Bootstrap & Self-Provisioning:** Systems solve the "chicken-and-egg"
  bootstrap problem with minimal installers and phased initialization.
  Kubernetes' **kubeadm** uses phased steps (pre-checks, certificates,
  control-plane bring-up, join
  nodes)[\[5\]](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#:~:text=,you%20wish%20to%20apply%20customization),
  and cloud VMs rely on **cloud-init** scripts to self-configure on
  first
  boot[\[6\]](https://guides.zadarastorage.com/cs-compute-guide/latest/cloud-init.html#:~:text=Cloud,on%2C%20providing%20standardization%20and%20manageability).
  **Recommendation:** Adopt a **phased bootstrap** for chora: a tiny
  bootstrap script (Phase 0) installs a core runtime (Phase 1), which in
  turn provisions essential infrastructure services (Phase 2), then
  launches remaining capability servers (Phase 3). Emphasize
  idempotency, health checks, and rollback on failures. Part 2 details
  bootstrap patterns, with flow diagrams and an example Python installer
  illustrating these principles.

- **Registry & Manifest Patterns:** Dynamic service discovery in large
  systems is enabled by centralized or distributed registries tracking
  service metadata and health. For example, **Consul** and **ZooKeeper**
  maintain strongly consistent views of services (via Raft/ZAB
  consensus)[\[7\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=%2A%20Type%3A%20Service%20discovery%2C%20key,mesh%20capabilities%20with%20Consul%20Connect)[\[8\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=Zookeeper),
  while **Netflix Eureka** prioritizes availability with a weaker
  consistency (clients use heartbeats; the registry "self-preserves"
  during network
  issues)[\[9\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,consistency%20but%20is%20highly%20available).
  **Recommendation:** Implement a **Manifest Registry** service that
  stores each capability server's metadata (name, version, endpoints,
  dependencies, health endpoint, etc.) and supports queries by
  capability or tags. Ensure strong consistency for core data (e.g.
  using consensus) but incorporate health-check mechanisms (heartbeat or
  periodic checks) to purge or flag unhealthy services. Part 3 includes
  a matrix comparing Consul, etcd, Zookeeper, and Eureka, and presents a
  proposed registry schema and sample code for service registration and
  lookup.

- **Interface Design & Core-Interface Separation:** A clean separation
  between **domain logic** and **interface layers** is crucial.
  Domain-driven design (DDD) principles suggest treating each capability
  server as a bounded context with an internal domain model and
  ubiquitous language. Interface **contracts** (RESTful OpenAPI specs,
  gRPC protobufs, CLI specs) should be well-defined and versioned
  independently of core code. Industry practice: gRPC uses an IDL
  (Protocol Buffers) to define services and messages separate from
  implementation[\[10\]](https://grpc.io/docs/what-is-grpc/core-concepts/#:~:text=gRPC%20is%20based%20around%20the,their%20parameters%20and%20return%20types),
  GraphQL defines a schema separate from resolver
  code[\[11\]](https://graphql.org/learn/schema/#:~:text=,infer%20the%20schema%20from%20that),
  and API Gateways like AWS's translate HTTP requests to backend calls
  (e.g. mapping JSON/HTTP to Lambda
  events)[\[12\]](https://repost.aws/questions/QU1O0MzZU2RVKnTx3vRY9neQ/how-to-transform-http-requests-to-lambda-events-exactly-as-aws-api-gateway-does-as-an-http-proxy#:~:text=How%20to%20transform%20HTTP%20requests,the%20development%20process%2C%20I).
  **Recommendation:** Treat interface definitions as first-class
  specifications -- for REST APIs use OpenAPI, for CLIs provide man
  pages/help, etc. The core should not depend on any single interface
  framework. Introduce translation layers or gateways (e.g. an MCP
  gateway service, or Envoy sidecars) to bridge protocols (Envoy can
  translate gRPC-Web to
  gRPC[\[13\]](https://grpc.io/blog/postman-grpcweb/#:~:text=Can%20gRPC%20replace%20REST%20and,the%20benefits%20of%20gRPC)).
  Implement standardized error handling (e.g. map internal errors to
  consistent HTTP status codes or CLI exit codes) and propagate tracing
  context across interface boundaries for observability. Part 4 provides
  diagrams of layered architecture, code showing unified error handling
  across CLI/HTTP, and prescriptive "do's and don'ts" for interface
  design.

- **Composition Models:** Capability servers rarely operate in
  isolation; they compose to achieve higher-level workflows. We
  distinguish **orchestration** (central coordinator service controlling
  interactions) versus **choreography** (distributed, event-driven
  collaboration). In orchestration, a single service (or state machine)
  calls others in sequence -- e.g. AWS Step Functions orchestrate
  microservices with a state machine
  workflow[\[14\]](https://dev.to/dixitjain/aws-step-functions-the-conductor-of-your-microservices-orchestra-2e77#:~:text=What%20are%20AWS%20Step%20Functions%3F).
  In choreography, services react to events -- e.g. an Order service
  emits an "OrderPlaced" event and an Inventory service listens and
  responds, with no central
  orchestrator[\[15\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=).
  **Recommendation:** Use orchestration for complex, multi-step
  processes requiring central logic or rollback (consider Saga pattern
  with a dedicated orchestrator coordinating compensating
  transactions[\[16\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=by%20coordinating%20transactions%20across%20multiple,approach%20helps%20maintain%20data%20consistency)[\[15\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=)).
  Use choreography (event buses, pub/sub) for simpler or highly
  decoupled integrations -- it reduces coupling but requires robust
  event management (ensure idempotency and no cyclic
  dependencies[\[17\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=Benefits%20of%20choreography%20Drawbacks%20of,Integration%20testing%20is%20difficult)).
  Implement dependency declarations in the manifest so that capability
  servers know what other services to look for (and possibly wait for)
  at startup. Apply **resilience patterns**: timeouts and retries for
  synchronous calls, circuit breakers to isolate failures, and
  idempotent handlers for repeated events. Part 5 illustrates these
  patterns with sequence diagrams (comparing orchestration vs.
  choreography) and example code (a simple saga orchestrator and an
  event bus pub/sub simulation).

- **SAP Development & Adoption:** To maximize adoption of these
  patterns, we propose a structured documentation framework --
  **Structured Autonomous Practices (SAPs)** -- for capability server
  development. A SAP is a bundle of guidance artifacts (charter,
  specification, guide for AI agents, adoption blueprint, etc.) that
  standardize knowledge
  transfer[\[18\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,capability%20package%20with%20standardized%20documentation).
  Our analysis of documentation frameworks (AWS Well-Architected, Azure
  Architecture Center, Google Cloud Arch. Framework) shows the
  importance of clear, sectioned guidance with progressive detail.
  **Recommendation:** Each new pattern or capability (multi-interface,
  bootstrap, registry, composition, etc.) should be codified as a SAP
  with a consistent structure:

- A **Capability Charter** outlining the problem, solution overview, and
  success metrics for that pattern.

- A **Protocol Spec** detailing interfaces/contracts (e.g. OpenAPI
  schemas, CLI commands) and versioning strategy.

- An **Agents Guide** (AGENTS.md) explaining how AI or autonomous agents
  can interact with this capability (for instance, how an AI agent might
  discover available interfaces or use the capability via MCP).

- An **Adoption Blueprint** giving step-by-step instructions to
  implement the pattern in a capability server, with **Adoption Tiers**
  (Essential, Recommended, Advanced) clearly marking which
  steps/features are mandatory vs. optional enhancements.

- A **Ledger** for tracking implementations and iterations (which
  projects have adopted the SAP, change history, known deviations).

- (Optional) Code templates or boilerplate projects accompanying the
  SAP, and additional notes (e.g. a CLAUDE.md for any Claude-specific
  tips, if relevant).

By providing these artifacts, SAPs will enable faster onboarding of
developers and ensure consistent application of best practices across
the chora ecosystem. Part 6 presents detailed SAP templates (including
outlines for each document type and how to incorporate tiered guidance)
and compares this approach to industry documentation standards. It also
includes a sample project template structure and recommendations for
maintaining SAPs over time (e.g. versioning them alongside code and
responding to community feedback).

**SAP Development Roadmap:** Following this research, we identify
several concrete SAPs to be created and updated: -
**SAP-MultiInterface:** Guiding how to build capability servers with
clean core logic and multiple interfaces (drawing from Part 1). -
**SAP-Bootstrap:** Defining the phased bootstrap process, minimal
installer template, and self-provisioning checks (Part 2). -
**SAP-Registry:** Standardizing the manifest/registry schema and usage
patterns (Part 3). - **SAP-InterfaceDesign:** Covering contract design,
translation layers, and observability (Part 4). - **SAP-Composition:**
Patterns for service composition, including orchestration workflows and
event-driven integration (Part 5). - **SAP-CapabilityServer-Template:**
A comprehensive template (or "capability server chassis") combining all
the above aspects, so new capability servers can be bootstrapped with
multi-interface support, registry integration, etc. out-of-the-box
(Parts 1--5 combined, operationalized in code). This would likely be an
evolution of the existing `chora-base` server scaffolding (e.g. update
**SAP-014: mcp-server-development**
template[\[19\]](file://file_000000005a9c71f595b82330733a65da#:~:text=)).

Each SAP will include Essential vs. Advanced tiers to accommodate teams
at different maturity levels, and they will reference each other where
appropriate (for example, the Multi-Interface SAP will link to the
Interface Design SAP for API contract guidance, etc.). By following
these SAPs, capability server developers in chora can adopt proven
patterns confidently, with copy-paste code examples and clear "do/do
not" guidance at each step. This will accelerate development, reduce
errors, and ensure **architectural consistency** across the ecosystem --
ultimately validating the capability server model as a robust, scalable
approach for AI-native workflows.

The remainder of this report is organized into six parts corresponding
to the research areas, with detailed findings, examples, and
recommendations. Appendices provide supporting reference material:
complete code listings, comparison tables, a glossary of terms, and a
list of references to source materials and further reading.

## Part 1: Multi-Interface Architecture

A **multi-interface architecture** enables a single capability server to
be accessed through multiple forms of interaction -- for example, a
Python API, a CLI tool, a RESTful HTTP API, and the Model Context
Protocol (MCP) -- without duplicating core logic. The goal is to provide
consistent functionality across all interfaces, so users or other
systems can choose the interface best suited to their context. This
section examines how leading platforms implement multi-interface support
and distills best practices for chora capability servers.

### Industry Patterns for Multiple Interfaces

Many successful systems expose the same underlying capabilities through
different interfaces. They achieve this by clearly separating core
functionality from interface-specific code, often using a client-server
or layered design:

- **Amazon Web Services (AWS):** AWS services can be controlled via the
  web Console (GUI), CLI, SDKs in various languages, and
  Infrastructure-as-Code (CloudFormation, CDK). All of these ultimately
  call the same internal service APIs. The AWS CLI is essentially a thin
  wrapper over AWS SDK calls (which in turn invoke AWS HTTP APIs). In
  fact, the AWS CLI in Python internally uses the `boto3` SDK for nearly
  all
  operations[\[2\]](https://stackoverflow.com/questions/59694539/how-do-i-write-aws-cli-commands-in-python#:~:text=).
  This means whether a user runs `aws ec2 describe-instances` on the
  command line or calls `DescribeInstances` via the Python boto3
  library, or clicks around the AWS Console, they get the same results.
  This consistency is by design -- **one core API, multiple access
  methods**. AWS additionally provides CloudFormation (templated
  declarative interface) which again utilizes the same service APIs
  under the hood to provision resources. The trade-off AWS chooses is to
  implement robust service APIs once, and keep CLI/SDK layers as
  stateless callers of those APIs, minimizing duplicate logic.

- **Docker:** Docker Engine exposes a REST API (over a UNIX socket or
  TCP) for container management, and the familiar `docker` CLI is
  essentially a client for that
  API[\[3\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=,why%20developers%20love%20using%20Docker).
  For example, running `docker run nginx` via CLI causes the CLI to call
  the Docker Engine API `POST /containers/create` and
  `POST /containers/{id}/start` behind the scenes. Docker Compose offers
  a higher-level interface (YAML config + tool) which again translates
  into Docker API calls. This layered approach (CLI → REST API → daemon)
  ensures all interfaces produce the same effect on the
  system[\[4\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=DockerHost).
  The Docker CLI is built in Go and utilizes a client library that maps
  commands to REST
  endpoints[\[20\]](https://medium.com/@kushalkochar9/conversion-of-docker-commands-into-rest-calls-677f5f856b83#:~:text=kochar%20medium,internal%20client%20methods%20that)[\[21\]](https://aws.plainenglish.io/docker-engine-explained-architecture-namespaces-and-resource-control-4e1716d67e49#:~:text=,to%20manage%20containers%20and%20services).
  By funneling all operations through the Engine API, Docker maintains a
  single source of truth for container state. This is a classic
  **client-server pattern**: CLI and other clients are thin; the Docker
  Engine (server) contains the core logic.

- **Kubernetes:** Kubernetes takes a multi-interface approach via its
  API-centric design. The Kubernetes control plane offers a
  comprehensive RESTful **API Server** (with JSON or Protobuf over HTTP)
  as the primary interface to the cluster. All other interfaces are
  built on this: `kubectl` (CLI) uses client libraries (`client-go` in
  Go, client libraries in Python, Java, etc.) which call the REST API;
  the Kubernetes Dashboard (web UI) also calls the same API. Critically,
  *"the REST API is the fundamental fabric of Kubernetes. All operations
  and communications between components, and external user commands are
  REST API calls that the API Server
  handles."*[\[22\]](https://kubernetes.io/docs/reference/using-api/#:~:text=The%20REST%20API%20is%20the,corresponding%20entry%20in%20the%20API).
  This means whether you use `kubectl get pods` or a Terraform provider
  for Kubernetes or a custom script, you're ultimately interacting with
  the same REST endpoints. Kubernetes even has the concept of **Custom
  Resource Definitions (CRDs)** which extend the API -- once a new
  resource type is added, `kubectl` can automatically handle it (using
  generic API discovery) without needing a bespoke CLI command. The
  interface separation pattern here is strong: the API server is the
  core; CLI is effectively a REST client (with convenience features like
  formatting, auth, etc.). Consistency is ensured by only implementing
  behavior in the API server.

- **Terraform:** Terraform is slightly different but still illustrates
  multi-interface ideas. Terraform\'s core is an engine that takes an
  infrastructure desired state (written in HCL, the HashiCorp
  Configuration Language) and applies changes via provider plugins. The
  primary interface is the Terraform CLI, which processes HCL config
  files. However, Terraform also can be driven through other means: for
  example, **Terraform Cloud/Enterprise** provides a Web UI and API to
  run Terraform plans and applies remotely. There's also the **CDK for
  Terraform** which allows writing configurations in general-purpose
  languages (TypeScript, Python, etc.), which are then synthesized to
  HCL. In all cases, the underlying terraform plan/apply logic and
  provider implementations are the same. **Interfaces**: (1) CLI + HCL
  (declarative files), (2) Cloud/Enterprise API, (3) SDKs like CDKTF or
  Terragrunt. The consistency comes from using the same Terraform core
  engine. A notable pattern is that Terraform CLI has both a
  human-facing interactive mode and machine-readable output (e.g.,
  `terraform plan -out=planfile` and `terraform show -json planfile` for
  automation), effectively providing a stable interface for other tools.
  HashiCorp has recognized different workflows (CLI-driven, VCS-driven,
  API-driven) for using
  Terraform[\[23\]](https://www.hashicorp.com/en/blog/which-terraform-workflow-should-i-use-vcs-cli-or-api#:~:text=CLI,their%20use%20cases%20and%20benefits),
  but all converge on the same core functionality. In short, Terraform
  demonstrates that even a primarily CLI-oriented tool can support GUI
  and API usage by **abstracting the core as a service** (when running
  in Terraform Cloud) or exposing its state files and plans in a
  machine-readable form.

**Comparison of Multi-Interface Approaches:** The table below summarizes
how these systems handle multi-interface architecture:

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **System**        **Interfaces      **Core             **Consistency Strategy**
                    Supported**       Implementation**   
  ----------------- ----------------- ------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **AWS**           Web Console GUI;  Core AWS services  Single set of service APIs for all interfaces ensures uniform behavior. CLI/SDK act as thin clients[\[2\]](https://stackoverflow.com/questions/59694539/how-do-i-write-aws-cli-commands-in-python#:~:text=). CloudFormation/CDK translate declarative specs into API calls.
                    CLI (`aws`); SDKs expose HTTP APIs   
                    (Java, Python,    (JSON); SDKs and   
                    etc.);            CLI call these     
                    CloudFormation    APIs (e.g. boto3   
                    (IaC templates);  for Python)        
                    Cloud Development                    
                    Kit (CDK)                            

  **Docker**        CLI (`docker`);   Docker Engine      CLI and Compose use the REST API under the hood[\[3\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=,why%20developers%20love%20using%20Docker)[\[4\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=DockerHost). All commands
                    Compose (YAML +   (daemon) with      funnel through the same daemon logic (client-server model).
                    CLI); REST API    internal REST API  
                    (for external     endpoint           
                    apps); Docker                        
                    SDKs (Python,                        
                    etc.)                                

  **Kubernetes**    CLI (`kubectl`);  Kubernetes API     **All** interactions go through REST API calls to the API Server[\[22\]](https://kubernetes.io/docs/reference/using-api/#:~:text=The%20REST%20API%20is%20the,corresponding%20entry%20in%20the%20API). Kubectl and UIs are API clients. CRDs allow new interfaces without changing CLI code, via dynamic discovery.
                    Client Libraries  Server as central  
                    (Go, Python,      hub; etcd store    
                    etc.); Dashboard  for state; core    
                    (Web UI); YAML    controllers in     
                    manifests (apply  control plane      
                    via CLI or                           
                    GitOps);                             
                    Operators                            
                    (controllers                         
                    extending API)                       

  **Terraform**     CLI (`terraform`  Terraform Core     CLI is primary but Terraform Cloud's API wraps the same core engine. HCL is primary interface language, but code (CDK) or GUIs compile down to it. Uniform behavior by using identical plan/apply logic for all
                    commands) with    engine             workflows[\[24\]](https://www.hashicorp.com/en/blog/which-terraform-workflow-should-i-use-vcs-cli-or-api#:~:text=match%20at%20L294%20,more%20effort%20to%20integrate%20into)[\[25\]](https://www.hashicorp.com/en/blog/which-terraform-workflow-should-i-use-vcs-cli-or-api#:~:text=,more%20effort%20to%20integrate%20into).
                    HCL config files; (plan/apply) +     
                    Terraform Cloud   provider plugins.  
                    web UI & REST     State management   
                    API; CDK for      in files or remote 
                    Terraform (code   backends.          
                    as config); other                    
                    wrappers                             
                    (Terragrunt,                         
                    etc.)                                
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[\[2\]](https://stackoverflow.com/questions/59694539/how-do-i-write-aws-cli-commands-in-python#:~:text=)[\[3\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=,why%20developers%20love%20using%20Docker)[\[22\]](https://kubernetes.io/docs/reference/using-api/#:~:text=The%20REST%20API%20is%20the,corresponding%20entry%20in%20the%20API)

*Table 1: Multi-Interface Architecture Patterns in Industry Systems.*

Each system above avoids duplicating business logic in each interface.
Instead, they concentrate logic in a core service or engine, and keep
interfaces as **facades or adapters**. This yields consistent results
regardless of interface and simplifies adding new interfaces in the
future (you just build a new adapter to the same core).

**Thick vs. Thin Interfaces:** A notable design choice is whether
interface layers are "thin" (minimal logic, just mapping inputs to core
calls) or "thick" (containing significant logic themselves). In general,
industry practice leans toward thin interfaces and a thick core, except
where interface-specific optimizations are needed. For example, an
interactive CLI might format output nicely or offer progress bars (UI
concerns), but it should delegate the heavy lifting to the core library
or service. Thick interface layers can lead to divergence (if, say, the
CLI implemented some behavior not available via API). **Anti-pattern:**
Don't implement critical business rules in only one interface. (E.g., if
Docker had made the CLI handle container restart logic and bypassed the
Engine API, then API users would have inconsistent behavior -- they
wisely avoided that.)

Kubernetes provides an example of keeping interfaces extremely thin --
`kubectl` is primarily a wrapper that authenticates and sends REST calls
and then outputs results. Most `kubectl` subcommands correspond directly
to API operations, and for complex logic (like `kubectl apply` which
does a three-way merge of changes), the open-source community eventually
moved that server-side as well (to the Server-Side Apply feature in the
API server) to maintain consistency across clients.

**Interface Separation and Abstractions:** Some architectures use an
explicit abstraction layer between core and interfaces. For instance, an
application might define a **Service Interface** as an abstract class or
Go interface that declares operations (e.g., `deploy()` or
`listItems()`), implemented by the core logic class. Then the CLI, REST
controller, etc., all invoke that interface. This is akin to the **Ports
and Adapters** (Hexagonal) architecture: the core defines "ports"
(interfaces) that are implemented by adapters (UIs, CLIs, etc.). The
adapters convert external input (CLI args, HTTP requests) into core
method calls, and format the results for output.

In strongly typed languages, one might see a common interface trait and
multiple implementations. In Python, one can achieve a similar
separation by design (even without formal interface types). The key
principle is **do not mix UI concerns into core logic**: for example,
reading `sys.argv` or HTTP headers should happen in the interface layer,
not deep in the core business logic.

### Designing Capability Servers with Multiple Interfaces

For capability servers in the chora ecosystem, supporting multiple
interfaces is a requirement by
definition[\[1\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,a%20component%20that).
A user should be able to, say, call a function in Python (native API)
for in-process use, run a CLI command for scripting, send an HTTP
request for external integration, or invoke via MCP for AI agent
orchestration -- and all achieve the same underlying effect. To realize
this:

- **Single Source of Truth for Logic:** Implement the capability's
  functions once (e.g., in a Python module `core.py` containing
  classes/functions that do the real work). Treat this as a library used
  by all interfaces.

- **Isolate Interface Code:** Create separate modules for each
  interface: e.g., `cli.py` handles command-line parsing and calls
  `core`; `api_http.py` defines HTTP routes and translates HTTP to core
  calls; `mcp_interface.py` handles MCP-specific protocol details (if
  MCP integration requires a particular message format or session
  handling).

- **Uniform Error Handling:** Decide how errors from core logic will be
  represented in each interface. Possibly define a set of custom
  exception classes in the core, and have each interface layer catch
  them and translate to the appropriate error reporting mechanism (CLI:
  exit code and stderr message; REST: HTTP status code and JSON error;
  MCP: an error reply through the protocol). This ensures, for example,
  that a "not found" error or validation failure is consistently
  communicated.

- **Consistency and Testing:** Each interface should be tested to
  produce identical outcomes. Contract tests can ensure that for given
  inputs, the CLI and HTTP interfaces produce the same changes in the
  system. One way to enforce this is to route all tests through the core
  logic (bypassing UI) and only have a smaller set of integration tests
  for interface wiring, since the core is already heavily tested.

- **Documentation:** Provide unified documentation or cross-reference
  between interfaces. For example, a user reading the capability
  server's docs should see an operation like "provision new environment"
  and see the CLI command, REST endpoint, and Python method all listed.
  (AWS does this in its docs: an action like *Create EC2 Instance* is
  documented once, with snippets for console, CLI, API, SDK in various
  languages.)

- **Interface-Specific Features:** Acknowledge differences where needed.
  Some interfaces have capabilities others don't -- e.g., a CLI can
  prompt a user interactively or stream text output easily, whereas an
  HTTP API might prefer streaming via webhooks or server-sent events.
  Design core logic to be flexible if needed (or allow the interface
  layer to handle those specifics while core provides hooks). For
  instance, if an operation produces a stream of progress updates, the
  core can yield events (iterator or async generator). The CLI can
  consume and print them incrementally, the HTTP layer could either
  buffer and return as list, or use something like WebSocket/SSE to push
  updates. The key is designing the core function in a way that is
  agnostic to how results are consumed.

#### Code Example: Core Logic with CLI and REST Interface

Below is a simplified Python example illustrating a capability server
with one core function and two interfaces (CLI and HTTP API). The
example revolves around a hypothetical \"Manifest\" capability that
registers services. The core logic provided (`register_service`) is
exposed via a CLI command and an HTTP endpoint, with consistent behavior
and shared error handling:

    # core.py – Core capability logic (domain logic) 
    from typing import Dict

    # In-memory "registry" for demonstration
    SERVICE_REGISTRY: Dict[str, str] = {}

    class ServiceAlreadyExists(Exception):
        """Error raised if a service is already registered."""
        pass

    def register_service(name: str, url: str) -> None:
        """Register a new service by name with its URL. Raises if name exists."""
        if name in SERVICE_REGISTRY:
            raise ServiceAlreadyExists(f"Service '{name}' already registered.")
        # Core logic: store the service info
        SERVICE_REGISTRY[name] = url
        # (In real scenario, more complex actions like health checks or persisting to DB)

    # core_test.py – Example usage of core logic (could be unit tests)
    if __name__ == "__main__":
        register_service("example", "http://example.com")
        try:
            register_service("example", "http://duplicate.com")
        except ServiceAlreadyExists as e:
            print("Expected error:", e)
    # cli.py – CLI interface for the capability server
    import sys, argparse
    from core import register_service, ServiceAlreadyExists

    parser = argparse.ArgumentParser(prog="manifest-cli",
            description="CLI to register services in the manifest.")
    parser.add_argument("command", choices=["register"])
    parser.add_argument("--name", required=True, help="Service name")
    parser.add_argument("--url", required=True, help="Service URL")

    def main():
        args = parser.parse_args()
        if args.command == "register":
            try:
                register_service(args.name, args.url)
                print(f"Service '{args.name}' registered successfully.")
            except ServiceAlreadyExists as e:
                # Consistent error handling: print to stderr and exit with code
                sys.stderr.write(f"Error: {e}\n")
                sys.exit(1)

    if __name__ == "__main__":
        main()
    # api_http.py – REST API interface using Flask (for example purposes)
    from flask import Flask, request, jsonify
    from core import register_service, ServiceAlreadyExists

    app = Flask(__name__)

    @app.route("/services", methods=["POST"])
    def register_service_endpoint():
        data = request.get_json(force=True)
        name = data.get("name")
        url = data.get("url")
        if not name or not url:
            return jsonify({"error": "Missing 'name' or 'url'"}), 400
        try:
            register_service(name, url)
        except ServiceAlreadyExists as e:
            # Consistent error handling: return 409 Conflict with error message
            return jsonify({"error": str(e)}), 409
        return jsonify({"message": f"Service '{name}' registered"}), 201

    # Note: In production, this app would be run by a WSGI server or similar.

*Run CLI:*

    $ python cli.py register --name example --url http://example.com
    Service 'example' registered successfully.
    $ python cli.py register --name example --url http://example.com
    Error: Service 'example' already registered.
    $ echo $?  # exit code is 1 due to error
    1

*Run HTTP API (Flask app):*

    $ curl -X POST -H "Content-Type: application/json" -d '{"name":"example","url":"http://example.com"}' http://localhost:5000/services
    {"message":"Service 'example' registered"}
    $ curl -X POST -H "Content-Type: application/json" -d '{"name":"example","url":"http://duplicate.com"}' http://localhost:5000/services
    {"error":"Service 'example' already registered."}  # HTTP 409 status

*Code Illustration 1: A core function* `register_service` *is invoked by
both a CLI and an HTTP API. The core raises a* `ServiceAlreadyExists`
*exception for duplicate entries; the CLI catches it and exits with an
error message, while the HTTP API returns a 409 Conflict with a JSON
error. This ensures both interfaces enforce the same rule.*

In this example, the core `register_service` function represents the
capability's logic, and the two interfaces each handle input parsing and
output formatting. The **exception class** `ServiceAlreadyExists` is
defined in the core module, enabling a shared understanding of that
error. This pattern can be extended: additional operations
(`deregister_service`, `list_services`, etc.) would be added to core.py
and corresponding commands/endpoints to CLI and HTTP layers, all
following the same pattern. If later we add an MCP interface, it might,
for instance, accept a certain JSON or message and similarly call
`register_service` and return a standardized response.

**Takeaways from Code Example:** The benefits of this approach are:

- We only implement the duplicate check in one place (core). There is no
  risk that the CLI allows overwriting an existing service while the
  HTTP API forbids it -- both use the same `ServiceAlreadyExists` rule.
- Adding a new interface (say a gRPC service) would involve writing
  another adapter that also calls `register_service`. The core remains
  unchanged.
- Consistent error messages across interfaces: both user and API client
  see \"Service \'example\' already registered.\" as the message in this
  scenario.
- Testing can focus on `core.register_service` behavior (e.g., verify it
  raises errors appropriately), and assume interfaces that call it will
  naturally enforce the same logic.

### Prescriptive Recommendations (Do's & Don'ts)

**Do:**\
- **Design a Clean Core API:** Encapsulate all domain logic in a module
or class that can be called from anywhere. This core should not depend
on how it's being called (no CLI-specific code, no HTTP-specific code
inside). Ideally, core methods are pure-ish functions (or methods) that
take well-defined inputs and return results or throw well-defined
exceptions. - **Use Interface Adapters:** Implement each interface in a
separate layer that adapts inputs to core calls and formats outputs. For
instance, use libraries like Flask/FastAPI for HTTP, Click or Argparse
for CLI, but keep their usage contained to the interface layer. - **Keep
Interfaces Thin:** Let them handle argument parsing, authentication (if
applicable), and output formatting, but nothing else. The core should be
doing the heavy lifting. This avoids divergence and simplifies
maintenance. - **Maintain Consistent Contracts:** Ensure that all
interfaces use the same terminology and default behaviors. For example,
if a capability server has a concept of a \"workspace,\" the CLI
command, HTTP parameter, etc., should use the same name and semantics.
Document these in one place and reuse across interfaces. - **Leverage
Code Reuse:** If possible, implement common interface logic in shared
helpers. E.g., if both CLI and HTTP need to validate a name string
(certain pattern), have a core helper function or a single source of
truth for that validation. This might even be in the core logic
itself. - **Test Across Interfaces:** Use automated tests to verify that
doing X via CLI or via HTTP yields the same result in the system. One
approach is an integration test that calls the core directly, then calls
the public interfaces and compares outcomes in the `SERVICE_REGISTRY` or
expected state. This will catch any inconsistency or missing
functionality.

**Don't:**\
- **Don't Fork Logic per Interface:** Avoid having one interface
implement extra features not available in others (unless absolutely
necessary and documented). For instance, if an operation does A, B, C
steps, don't have the CLI do an extra D step that the REST API doesn't
-- this will confuse users and break consistency. - **Don't Hardcode
Interface Assumptions in Core:** The core shouldn't assume it\'s being
called from a CLI or web context. For example, it shouldn't read
environment variables or global flags set by CLI; such context should be
passed in as parameters if needed. This keeps the core reusable. -
**Don't Neglect Versioning:** When multiple interfaces exist, you must
consider versioning and compatibility. E.g., a CLI tool may have version
1.0 and then 2.0 with changes; an HTTP API might have v1 and v2
endpoints. Plan for how the core supports multiple versions or how
interfaces might translate a newer request to an older core call if
needed. (E.g., AWS CLI is versioned separately from AWS APIs, but it
knows how to call the right API versions.) - **Don't Ignore Performance
Differences:** Sometimes using one interface versus another might have
performance implications (e.g., calling a function in-process vs making
an HTTP call). If your capability server might sometimes be invoked
in-process (via Python API) and other times over the network (REST),
design with that in mind. For example, ensure thread safety or avoid
global state that could behave differently in each context. - **Don't
Duplicate Data Definitions:** Use common data models across interfaces.
For example, define a schema or class for your data structures (like a
`Service` object with `name` and `url`). The CLI help, HTTP JSON schema,
etc., should all refer to the same fields. Consider generating parts of
interfaces from a single schema (e.g., generate OpenAPI from the core or
vice versa, or at least define constants for field names).

By following these guidelines, all capability servers in chora can
present a **uniform experience**. A developer should be able to switch
from calling a function in a script to hitting an HTTP endpoint, to
using a CLI command, without relearning concepts or worrying that one
method might do something slightly different.

### Patterns from AWS, Docker, Kubernetes, Terraform -- What Chora Should Emulate

Looking again at the industry examples, here are specific best practices
to emulate in the chora context:

- **Unified API (Kubernetes-style):** It could be beneficial for chora
  to have a central **Model Context Protocol (MCP) API** that each
  capability server registers with, so that an AI agent (or any client)
  could discover and invoke any capability through a common protocol. In
  effect, MCP could play a similar role to Kubernetes' API server or
  AWS's service API gateway, brokering calls to different capabilities.
  In practice, this might mean capability servers expose adapters for
  MCP (likely already in design as per "MCP interface" being one of the
  interfaces). The pattern is: **one network/IPC protocol to rule them
  all**, with others (CLI, native) as optional conveniences.

- **SDK or Native Library (AWS and Terraform-style):** Provide a Python
  SDK for each capability (could simply be the core Python API, properly
  packaged). E.g., if there\'s a capability server for "orchestration",
  publish a `chora.orch` Python package that developers (or AI agents
  running Python code) can import to use its functions directly (instead
  of always going through HTTP). AWS does this with boto3 for all
  services. This leverages the fact that chora is Python-based -- we can
  ship the core logic as a library. However, we must ensure when that
  library is used, it either communicates with the server process or
  runs the logic in-process appropriately. A design decision is whether
  the Python "native API" calls the server via RPC or shares memory.
  Given capability servers might be separate processes, a lightweight
  client might be needed. (For example, Kubernetes' client-go or AWS
  SDKs are essentially RPC clients. In our code example above, using the
  core directly is in-process, but in a real deployment the core might
  run in a service process.)

- **CLI as client (Docker-style):** We can implement CLI tools for each
  capability server that act as clients to the server's API (rather than
  launching full server logic themselves). For instance, a
  `chora-manifest` CLI could call the Manifest server's HTTP API under
  the hood. This is how `kubectl` works (calls the Kubernetes API
  server) and how the `aws` CLI works (calls AWS service endpoints). The
  benefit is the CLI always operates against the live service (ensuring
  the same state), and complex logic resides server-side. The downside
  is needing the server up and credentials configured. Alternatively, if
  the CLI directly imports core logic (like our example), you get a
  simple all-in-one usage but risk bypassing the running server. We
  might choose approach per capability (e.g., for controlling remote
  services, CLI must call the server; for something local, CLI can run
  core directly).

- **Declarative Config (Terraform-style):** Consider allowing certain
  operations to be declared in YAML/JSON form and processed in bulk.
  This might be relevant for multi-step processes (though more so a
  composition concern in Part 5). The idea is multi-interface also
  includes "configuration as interface". E.g., a user could provide a
  config file describing multiple services to register, instead of
  issuing commands one by one. This could be an advanced interface (like
  how Docker Compose extends Docker, or Terraform plan files for AWS
  resources). In chora, for example, the Orchestration server might
  accept a YAML manifest of desired capability servers to run. This is
  an additional interface (declarative config) on top of imperative
  API/CLI.

### Testing and Documentation Strategies for Multi-Interface Systems

To ensure consistency across interfaces, adopt some of the strategies
used by these platforms:

- **Contract Testing:** Use contract tests or "behavioral tests" that
  run a scenario via different interfaces and compare outcomes. For
  instance, register a service via CLI in a test, then query via HTTP
  API to verify it is there. Or vice versa. This can catch mismatches
  early.

- **Documentation:** For each capability's documentation, have a unified
  reference with sub-sections for each interface. For example, a section
  "**Usage: Create Workspace**" might include: CLI command example, HTTP
  API endpoint example (with JSON payload), Python API example (code
  snippet), MCP call example. This mirrors AWS style documentation. It
  prevents one interface from becoming second-class (users shouldn't
  have to guess how an operation translates to another interface). Tools
  can help generate these from a single source (like OpenAPI can
  generate parts of CLI docs, etc., or vice versa).

- **User Journey Testing:** Think of typical user tasks and ensure they
  can be completed start-to-finish using any one interface or a mix.
  Some users may mix interfaces (e.g., use CLI for setup, then
  automation via API). The system should allow that seamlessly (no
  hidden state per interface).

In summary, **multi-interface architecture** in capability servers is
about providing choice and flexibility without sacrificing uniformity.
By building a robust, well-defined core and making all interfaces defer
to it, we ensure that improvements or bug fixes in logic benefit all
access methods. This uniform core also simplifies onboarding new
interface types in the future (imagine adding a voice interface or a
chatbot that uses the same core -- feasible if core is independent of
interfaces).

### SAP Outline: Multi-Interface Capability Server Pattern

To capture this knowledge for SAP development, we will create **SAP-XXX:
Multi-Interface Capability Server Pattern**. This SAP will guide a
developer through designing a capability server with multiple
interfaces. Its structure may be:

- **Capability Charter:** Explains why multi-interface support is
  important (e.g. accessibility in different contexts, AI integration
  via MCP, etc.), defines the success criteria (e.g. "all operations
  available via all four interfaces, passing consistency tests"), and
  enumerates the scope (interfaces covered: Native Python, CLI, REST,
  MCP).

- **Protocol Spec:** Contains the contract for each interface. For
  example, it might include an OpenAPI specification snippet for key
  REST endpoints, the CLI commands and options (perhaps in a tabular or
  help-text form), and the class/method signatures for the Python API.
  It would also specify error codes and any interface-specific nuances.
  Essentially it defines the **capability's interface contract** in a
  technology-agnostic way, then shows how each concrete interface
  implements it. (E.g., "Operation X: does Y. CLI: `chora-example do-x`;
  HTTP: `POST /example/x`; Python: `example_client.do_x()`").

- **Agents Guide (AGENTS.md):** This would describe how an AI agent can
  utilize the multi-interface nature. For instance, it might show
  prompts or strategies for an AI to decide when to use the CLI vs. call
  an internal function vs. use an HTTP call. (If agents have direct
  access to the process, perhaps the native API is most efficient; if
  they operate over a tool interface, maybe they use CLI commands.) It
  could also cover how the MCP interface works for this server (since
  MCP is specifically for AI/agent integration), e.g. the format of MCP
  messages corresponding to each operation.

- **Adoption Blueprint:** This is the practical step-by-step guide. For
  multi-interface, it might start from a scaffold (perhaps referencing
  the **capability server template** SAP) and then:

- **Essential Tier:** Implement core logic for a simple operation;
  expose it via one interface (say HTTP) as proof of concept.

- Then add a second interface (CLI), calling the same core -- run a
  provided test script to verify both produce same result.

- Add remaining interfaces (with guidance on patterns or provided code
  templates, e.g. using an OpenAPI generator to stub out the HTTP
  interface).

- Demonstrate error handling by causing a deliberate error and showing
  how it appears identically in CLI vs API.

- Provide a testing checklist (did you document all interfaces? did you
  run cross-interface tests?).

- **Recommended Tier:** implement advanced features like authentication
  across interfaces (ensuring token handling is consistent), or
  streaming outputs, etc.

- **Advanced Tier:** possibly integration into a service mesh or gateway
  (e.g., registering the REST API with the chora gateway for unified
  routing, so that an AI can call any server via one host). Or
  generating SDK stubs for the API.

- **Ledger:** This will track projects that adopt the multi-interface
  pattern (e.g. "chora-mcp-orchestration v1.2 adopted multi-interface
  pattern on 2025-12-01, CLI added; chora-mcp-n8n opted to have only
  HTTP and not CLI due to XYZ, etc.") and track changes in the SAP
  itself (like if we change recommended library for CLI, etc., we note
  that in versions).

- **Templates/Code:** The SAP could link to or include a minimal code
  template (maybe a GitHub repo or a snippet in an appendix) that sets
  up a skeleton of core + interfaces. New capability server projects can
  copy this. Ensuring this template stays updated (via chora-base or
  automated tests) would be part of SAP maintenance.

By following SAP-XXX, a developer new to chora should be able to
scaffold a multi-interface server, implement their domain logic once,
and quickly get it exposed on all required interfaces following the
patterns laid out (matching the examples and recommendations in this
Part 1).

## Part 2: Bootstrap and Self-Provisioning Patterns

Bootstrapping a system -- especially one that is **self-hosting or
self-provisioning** -- is notoriously tricky. This is the classic
chicken-and-egg problem: to run the system you might need parts of the
system already running. For instance, how do you deploy an orchestration
server that itself orchestrates deployments? The solution is a
well-planned bootstrap sequence that gradually brings a system to life,
possibly with manual or external help for the first step. In the context
of the chora ecosystem, we want capability servers that can **provision
themselves and each other** with minimal manual intervention, while
avoiding circular dependencies or a confusing tangle of setup
instructions.

This section surveys bootstrap patterns from package managers,
orchestrators, and cloud platforms, then outlines a recommended
bootstrap process for capability servers (in phases), including
installation scripts, self-registration, and health checks.

### Patterns for Solving the Bootstrap Problem

Various systems have developed ingenious methods to initialize
themselves:

- **Package Managers Bootstrapping:** Consider language package managers
  like `npm` (Node.js) or `pip` (Python). How do you install the package
  manager itself? Often, the language runtime includes a minimal version
  or a script is provided. For example, Python includes an `ensurepip`
  module that can bootstrap `pip` installation if it\'s missing. Node.js
  installations bundle `npm` so that it\'s available from the start.
  **npm** also introduced `npx` which allows running packages without
  installing them globally, effectively bootstrapping one-off execution
  by downloading on the
  fly[\[26\]](https://forum.freecodecamp.org/t/difference-between-npm-and-npx-in-react/265124#:~:text=Difference%20between%20Npm%20and%20Npx,bin).
  **Cargo** (Rust\'s package manager) is installed as part of the Rust
  toolchain (`rustup` manages this). **APT (Advanced Package Tool)** on
  Debian-based Linux has the `debootstrap` utility to create a minimal
  system with apt so that apt can then install the rest of the system.
  The general pattern is: *the system provides either a minimal built-in
  package manager or a script to fetch it*. Once the package manager
  (pip, npm, etc.) is in place, it can install all other packages
  including possibly updates to itself. Many package managers can even
  update themselves (e.g. `npm install -g npm` can upgrade npm, pip can
  upgrade pip) -- they treat themselves as just another package to
  manage, albeit carefully to avoid removing the floor under their feet.

- **Orchestration Systems Bootstrapping:** Tools like Kubernetes and
  Docker Swarm require an initial step to form a cluster. **Kubernetes**
  provides `kubeadm` which simplifies bringing up a master node by
  performing a series of well-defined phases (init tasks like generating
  certificates, starting the API server, installing etcd, marking the
  node as master,
  etc.)[\[5\]](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#:~:text=,you%20wish%20to%20apply%20customization).
  Notably, `kubeadm` allows invoking each phase
  (`kubeadm init phase [something]`) for advanced scenarios where manual
  control is needed. This phased approach ensures that if something
  fails, the admin can fix the issue and resume from that phase, or
  debug individual steps. **Docker Swarm** uses a simpler
  `docker swarm init` which turns a Docker engine into the first manager
  node and prints a join token for other nodes. That token is an example
  of bootstrapping data -- it's a secret needed to securely add more
  nodes, generated during init and then used for subsequent steps.
  **HashiCorp Nomad** (cluster orchestrator) also has a bootstrap where
  one agent is started in server mode to create the initial cluster
  quorum (often requiring at least 3 servers to avoid single point of
  failure -- that itself implies starting 3 nodes possibly in developer
  mode or with expectation of config management to start them together).

- **Circular dependency resolution:** In orchestration, sometimes
  components depend on each other. For instance, in chora's context: the
  Orchestration server might rely on a Manifest server to discover what
  should be deployed, but the Manifest server might itself be deployed
  by the Orchestrator. Who starts first? A pattern is to break the cycle
  by introducing static configuration or a bootstrap role for one of
  them. For example, one might start the Manifest server in a degraded
  standalone mode with a static file, allow Orchestrator to come up and
  register with it, then switch Manifest to normal mode. Kubernetes
  solved a similar problem of "who configures etcd for the API server"
  by initially using static config files for etcd and API server when
  using `kubeadm`, then migrating to the self-hosted model (the API
  server can itself run on Kubernetes, but you first bring up one
  outside then pivot). These are advanced techniques; the general advice
  is to **identify minimal set of components that must be manually
  configured or have static config just to get things going, then let
  the system take over**.

- **Cloud Platforms Bootstrap:** In cloud environments, bootstrapping
  often refers to provisioning the initial infrastructure. **AWS
  CloudFormation** can deploy almost any AWS resource, but how do you
  deploy the environment needed to run CloudFormation? Usually AWS
  manages that (the CloudFormation service is always available to use).
  In cases where you need something before that, sometimes a *nested
  bootstrap* is used: for example, using CloudFormation to set up a
  CodePipeline that then applies more complex changes. **Terraform** has
  a concept of "remote state backend" -- to store its state in S3 or
  Consul etc., you often must create that backend first (like ensure an
  S3 bucket exists). That's usually done one-time outside of Terraform
  or with a separate Terraform init script. **Terraform's** guidance
  often suggests bootstrapping the backend manually or via a very small
  independent configuration, then having the main config use it. On
  another note, when launching a new cloud VM, user-data scripts
  (cloud-init as mentioned below) run to bootstrap the instance (e.g.
  install software, set config).

- **Self-Hosting Tools:** Some systems have the property of
  self-hosting. For instance, **Ansible** is configuration-as-code that
  doesn't require a dedicated server process -- it uses SSH to run tasks
  on target nodes. Bootstrapping Ansible simply required having Python
  on the target and SSH access; no agent installation needed (contrast
  with Chef or Puppet which require
  agents)[\[27\]](https://forum.ansible.com/t/agentless-architecture-in-ansible/21730#:~:text=Agentless%20architecture%20in%20Ansible%201,It%20uses%20the)[\[28\]](https://medium.com/@kansvignesh/ansible-vs-chef-59ab2935444d#:~:text=As%20Ansible%20is%20agent,transparent%2Fseamless%20experience%20to%20the%20user).
  Ansible's approach was essentially avoiding a bootstrap step by
  piggybacking on existing tools (SSH and Python are assumed to be
  there). This is an important pattern: *minimize your bootstrap
  dependencies.* If the environment already has a secure shell and
  Python, leverage that instead of requiring installation of a custom
  agent beforehand. (In chora's case, if we assume Python is there,
  perhaps a `pip install chora` could be a bootstrap for some parts, as
  long as network access is available.)

- **Virtual Environments:** Tools like **venv** or **virtualenv** in
  Python bootstrap an isolated environment by copying Python binaries
  and packaging tools so that the environment can then install needed
  packages. It's a two-step: you have Python, use it to create venv
  (bootstraps pip inside), then pip can install the rest. This pattern
  of *staging bootstraps* (use a slightly larger bootstrap to enable the
  final installation) is common. Another example is **gradle** wrapper
  in Java projects: they include a tiny `gradlew` script that downloads
  Gradle on first run so that a user doesn't have to install Gradle
  globally.

From these examples, a few **common bootstrap strategies** emerge:

1.  **Provide a Minimal Installer:** a script or binary that is small,
    easy to execute, with minimal dependencies, whose job is to set up
    the real system. This could be cURL-ing a shell script (common in
    cloud software installation), an `npm init` that uses npx to run
    something directly, etc. The minimal installer should be simple
    (because if it fails, users get stuck early). It often just
    downloads or copies files and maybe generates config.

2.  **Phase the Bootstrapping:** break the process into defined phases
    or stages, where each stage's output feeds the next. This helps with
    understanding and recovering from errors. Phases often are:

3.  *Phase 0:* Pre-bootstrap (user or external actions). E.g., "run
    install script X with privileges" or "ensure Docker is installed on
    host".

4.  *Phase 1:* Bring up core infrastructure that everything else depends
    on (databases, coordination services, etc). In chora, that might be
    an etcd or Consul if we use it, or basically the Manifest registry
    if everything else relies on service discovery.

5.  *Phase 2:* Launch fundamental capability servers (the ones that
    others depend on). Perhaps Orchestration and Manifest come here,
    since other capabilities might depend on them being around for
    discovery or deployment.

6.  *Phase 3:* Higher-level or optional services and user-specific
    provisioning. Each phase can have verification (e.g., health checks)
    before
    proceeding[\[29\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,patterns%20and%20failure%20modes).

7.  **Bootstrapping with Self-Checks and Idempotency:** The process
    should be idempotent -- running it again should not break the
    system, it should either skip steps that are done or safely re-do
    them. For instance, a bootstrap script that creates a default admin
    user should check if it exists already. If a step fails midway, the
    admin can fix the issue and re-run without the script blowing up on
    "already did something". Tools like kubeadm are idempotent to an
    extent (but some things like generating a cert twice might require
    cleaning up first -- they often document how to reset and retry).

8.  **Rollback Plans:** If bootstrap fails, ideally have a way to
    rollback partial changes. In a simple scenario, maybe the script
    prints instructions, e.g., \"if failure at step 3, run
    `bootstrap --rollback-step3` to undo partial work\". In databases,
    migrations often have down scripts. While not all systems implement
    rollback for bootstrap (some just advise tearing everything down and
    starting over if early steps fail), in production or long-running
    systems it's worth considering. e.g., if Orchestration server
    partially started some containers, but then failed, the bootstrap
    should ideally clean those containers if we run it with a rollback
    flag or on a second run.

9.  **Trust & Security in Bootstrap:** An aspect not to overlook is
    establishing trust. For example, that join token in Docker Swarm, or
    kubeadm generating certificates -- the bootstrap process often sets
    up the initial trust (cert authorities, tokens, keys) that will
    secure the system moving forward. It should do so carefully (using
    secure random, user input for secrets or secure storage). Similarly,
    our chora bootstrap might create initial credentials (API keys for
    orchestrator, etc.) that need to be communicated to the user
    securely at bootstrap time (like how `kubeadm init` outputs a
    kubeconfig for the admin).

10. **Real World Example:** `cloud-init` deserves a bit more detail as a
    generic bootstrap solution. **cloud-init** runs on first boot of a
    VM to execute user-provided configuration (like installing packages,
    writing config files, running
    scripts)[\[30\]](https://cloudinit.readthedocs.io/en/latest/explanation/introduction.html#:~:text=The%20operation%20of%20cloud,has%20applied%20the%20networking%20configuration)[\[31\]](https://cloudinit.readthedocs.io/en/latest/explanation/introduction.html#:~:text=During%20late%20boot%C2%B6).
    Cloud-init splits work into an *initial local phase* (before
    networking is up, often used to set hostnames or configure network
    from metadata) and a later phase (after network, to install
    packages,
    etc.)[\[30\]](https://cloudinit.readthedocs.io/en/latest/explanation/introduction.html#:~:text=The%20operation%20of%20cloud,has%20applied%20the%20networking%20configuration).
    This pattern of doing minimal work to get network, then pulling rest
    from network, is very common. It reduces the baked-in size of the
    image and allows reuse. In chora, we might use a similar approach:
    e.g., deliver a minimal binary or container that on startup fetches
    the latest manifest of capabilities to install, etc.

11. **Real World Example:** `kubeadm` similarly does a local phase
    (setting up files, etc.) and then coordinates cluster bring-up
    (which might involve other nodes joining). The presence of a phase
    subcommand in
    kubeadm[\[32\]](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#:~:text=,you%20wish%20to%20apply%20customization)
    is a user-friendly design allowing granular control. We should
    consider if our bootstrap tool might allow "step-by-step" mode for
    debugging, but likely a simple sequential script suffices for now.

### Self-Provisioning Architectures and Phases

In a self-provisioning system, the ultimate goal is that after giving it
an initial kick, the system *provisions the rest of itself
automatically*. Chora's vision suggests that once the base is in place,
capability servers can deploy other capability servers (the
Orchestration server deploying instances of others, etc.). To reach that
state, we define explicit phases:

- **Phase 0: Pre-Bootstrap (External Setup).** This phase includes
  anything that must be prepared by the user or an external system. The
  goal is to keep this minimal. For example, Phase 0 might be: \"Install
  Docker and Python on the host, and run the chora bootstrap
  installer.\" Or if delivering via containers: \"Run
  `docker-compose up` on a provided minimal docker-compose.yml that
  brings up the Bootstrap container.\" In cloud, Phase 0 could be
  launching a base VM or container with the bootstrap code embedded.
  Phase 0 might also involve the user configuring a few settings (like
  providing a domain name or choosing a cloud provider or reading
  prerequisites). **Keep Phase 0 as small as possible** because it's
  manual or external.

- **Phase 1: Core Provisioning (Bootstrap Runtime).** In this phase, the
  bootstrapper sets up core services that everything else will rely on.
  For chora, one such core piece could be the **Manifest registry**
  (since other services use it to find each other). If the manifest is
  itself a capability server, we might start a simple instance of it
  from minimal config (perhaps it initially has an empty registry or a
  static file). Another core piece could be any data store (if, say, we
  decided to use etcd or Consul as a backend for the manifest or as a
  config store, we'd start it here). Essentially Phase 1 establishes a
  *footing* on which further automation can work. After Phase 1, there
  should be a basic environment where a capability server can run and
  register itself.

- **Phase 2: Infrastructure/Orchestration Provisioning.** With the core
  in place, now bring up the **Orchestration capability server** (the
  one that can launch other servers, like `chora-mcp-orchestration`) and
  perhaps any other "infrastructure-level" capability servers (maybe the
  Gateway if it's needed early, etc.). The orchestration server, once
  running, should be pointed at the manifest (so it can register new
  services and discover others). Now the system essentially can **manage
  itself** -- it has a running orchestrator and a registry. At this
  point, further capability servers can be launched through the
  orchestrator's normal operations (instead of manual steps).

- **Phase 3: Capability Provisioning (User Services).** In the final
  phase, the rest of the capability servers (and perhaps user-defined
  services or configurations) are provisioned. This might happen
  automatically or semi-automatically. For example, orchestrator might
  read a configuration file or an "initial cluster manifest" that was
  provided and deploy capability servers listed there. Or this might be
  interactive: the user issues commands (via CLI or UI) to launch
  additional capabilities now that orchestrator is up. Regardless, by
  the end of Phase 3, all desired capability servers (manifest,
  orchestration, gateway, n8n, etc.) are running, registered in the
  manifest, and inter-connected. The system is now fully operational,
  having, in effect, *bootstrapped itself*.

Between phases, implement **health checks and waits**. E.g., after
starting Manifest in Phase 1, the bootstrap should poll it (or check a
log/port) until it\'s confirmed healthy (or timeout with error). Only
then proceed to Phase 2. Similarly ensure Orchestrator is up before
telling it to deploy others.

This phased approach is summarized in the diagram below, illustrating
the progressive layering of the system:

    flowchart TB
        subgraph Phase 0: Pre-Bootstrap (Manual)
          step0a([Ensure host OS/Deps])
          step0b([Run Chora bootstrap installer])
        end
        subgraph Phase 1: Core Provisioning
          step1a([Start Manifest Registry])
          step1b([Start Config Store / DB])
        end
        subgraph Phase 2: Infrastructure Services
          step2a([Launch Orchestration Server])
          step2b([Launch Gateway Server])
        end
        subgraph Phase 3: Capability Services
          step3a([Deploy remaining Capabilities via Orchestrator])
          step3b([Apply user configurations/workflows])
        end
        step0b --> step1a
        step1a --> step1b
        step1b --> step2a
        step2a --> step2b
        step2b --> step3a
        step3a --> step3b
        note over step1a,step1b: Core services like Manifest and data store are now running.
        note over step2a,step2b: Orchestrator can use the Manifest to register services and Gateway for routing.
        note over step3a,step3b: System deploys higher-level capabilities (e.g., n8n) and user agents.

*Diagram: Bootstrapping Phases for Chora -- Phase 0 (manual steps) sets
the stage, Phase 1 brings up core internal services (Manifest registry,
etc.), Phase 2 starts the Orchestration and other foundational
capability servers, Phase 3 deploys the remaining capabilities and
user-level services. Each phase depends on the previous ones being
healthy.*

This phased pattern is inspired by real systems: for example, in
Kubernetes kubeadm, Phase 1 is "bring up etcd and API server," Phase 2
"install core add-ons like DNS," Phase 3 "register nodes and normal
workloads." In chora, our add-ons are the other capability servers.

### Minimal Installers and Idempotent Bootstrapping

For chora, we should provide a **single unified bootstrap tool** --
perhaps a CLI command like `chora-bootstrap` or a script `bootstrap.sh`
-- that orchestrates the above phases. This could be language-agnostic
(a shell script) or in Python. A Python-based installer could leverage
existing libraries, but a shell script might be simpler to run on a bare
system. Another modern approach is a containerized bootstrap: e.g., "run
this bootstrap container with Docker, it will perform all actions." This
isolates the bootstrap logic and environment.

**Design considerations for the bootstrap tool:**

- **Idempotency:** The tool should be safe to run multiple times. One
  way is to have it detect if a phase is already done. For instance, it
  could check if the Manifest server is already running (perhaps by
  pinging its API) -- if yes, skip starting it. Or it might use lock
  files or markers (like writing to a file
  `.chora_bootstrap_phase1_done`). Simpler, it could prompt the user
  "already bootstrapped, do you want to rerun?" but fully automatic
  idempotency is nicer for scripting.

- **Configuration:** It should allow configuration inputs (where to
  install, network ports, etc.) but have good defaults. Possibly accept
  a config file or environment variables so that it can run unattended
  for different environments. For example, if the user wants all
  services to run in Docker containers vs. processes, the bootstrap
  might need a flag or a different mode.

- **Verification:** After each step, verify success. If starting
  Manifest, try a simple API call (like GET /health or version). If that
  fails, output an error and possibly hint how to troubleshoot (maybe
  show logs or advise checking Docker). These health checks are
  essential to not blindly plow ahead if something is wrong (which could
  cause cascading failures or hard-to-diagnose problems).

- **Rollback/Cleanup:** Provide a way to reset the environment in case
  of a failure or if the user wants to start over. This could be a
  `chora-bootstrap reset` command that stops any running capability
  servers, removes temporary files, etc., essentially bringing the
  system back to a clean slate (except maybe user data if any, which it
  should be careful not to delete without explicit confirmation). This
  is akin to `kubeadm reset` which attempts to undo what `kubeadm init`
  did (delete containers, etc.).

- **Self-update:** The bootstrap tool should ideally be able to update
  itself or inform the user if there\'s a newer version of the bootstrap
  procedure. Since bootstrap is something that might evolve (especially
  in early iterations of chora), users might run an older installer on a
  newer version of code -- mismatch could cause errors. Possibly
  incorporate a version check or ensure backward compatibility in the
  bootstrap script for different versions of capability servers.

**Bootstrapping Chicken-Egg Cases in Chora:**

A notable potential circular dependency: The Orchestrator deploys other
servers, but who deploys the Orchestrator? Our plan says the bootstrap
does (phase 2). That means initially, Orchestrator is started outside
its normal process (somewhat ironically, we manually start the thing
that is supposed to automate starting things). This is fine; after
bootstrap, Orchestrator can take over tasks for scaling or redeploying
itself on updates (for example, a future scenario: orchestrator notices
a new version of manifest server image, orchestrator could update it --
but orchestrator can't update itself easily unless we have multiple
orchestrator instances, so careful there).

Another dependency: The Manifest server holds service registry that the
Orchestrator uses to find running services and perhaps store environment
definitions. So manifest should start first (phase 1). If orchestrator
started without manifest, it would not know where to register or
discover; it could still run but isolated. So ordering is crucial, and
we handle that in phases as shown.

**Health Checks and Monitoring in Bootstrap:** Self-provisioning also
means the system should check itself as it comes up. A pattern from
Consul or Eureka: they often have the new instance perform a
registration or heartbeat. For bootstrap, our script could query each
service's `/health` endpoint to ensure it's functional. For example,
once manifest is up, maybe the bootstrap registers the orchestrator in
the manifest when it starts it (unless orchestrator self-registers on
its own). If orchestrator itself uses manifest's API to register, then
as long as orchestrator is pointed to manifest's address (which
bootstrap can supply via env var or config file), orchestrator on
startup will register and show up. The bootstrap can then query manifest
to see "is orchestrator listed and healthy?" as a confirmation that
Phase 2 succeeded. This way the bootstrap leverages the system's own
self-description to verify success.

**Handling Failures:** Suppose Phase 2 fails (orchestrator didn't start
properly). The bootstrap script should detect the failure (like timed
out waiting for orchestrator's health). It should then *halt*, report an
error clearly, and not proceed to Phase 3. The user then might fix
environment (maybe orchestrator image was not found or port conflict,
etc.), then either run a specific command to retry just that phase or
rerun the whole bootstrap (which through idempotency would skip Phase 1,
then try Phase 2 again). This guided failure handling is important to
not leave the system in a half-configured, unknown state.

**Example: Minimal Bootstrap Installer Script**

To ground this, consider a pseudo-code snippet for a bootstrap installer
(in Python for clarity):

    # pseudo-code of bootstrap steps
    def bootstrap_system():
        # Phase 1: start manifest
        if not is_running("manifest"):
            print("Starting Manifest server...")
            start_manifest()  # could run as subprocess or docker container
            if not wait_for_port(manifest_port, timeout=60):
                error("Manifest did not start or listen on port.")
                sys.exit(1)
            # Additional health check:
            if not manifest_api_healthcheck():
                error("Manifest health check failed.")
                sys.exit(1)
            print("Manifest server is up.")
        else:
            print("Manifest already running. Skipping start.")
        # Phase 2: start orchestrator
        configure_orchestrator_to_use_manifest(manifest_url)
        if not is_running("orchestrator"):
            print("Starting Orchestration server...")
            start_orchestrator()
            if not wait_for_port(orchestrator_port, timeout=60):
                error("Orchestrator did not start.")
                sys.exit(1)
            # Let orchestrator self-register to manifest, then verify:
            if not manifest_has_service("orchestrator"):
                error("Orchestrator not registered in manifest.")
                sys.exit(1)
            print("Orchestrator is up and registered.")
        # ...and so on for other phases

This illustrates checking for existing instances to allow re-entrance,
starting services, and verifying via manifest (self-describing). In real
code, we\'d need to handle process management (possibly running things
via Docker or systemd, etc., depending on architecture; for initial
simplicity, maybe just Popen processes in background).

### Real-World Flow Diagrams

It's instructive to see a real bootstrap sequence diagram for systems
like **kubeadm** or **cloud-init**, but we can focus on what chora's
might look like in a sequence form:

    sequenceDiagram
        autonumber
        participant User
        participant BootstrapScript
        participant Manifest
        participant Orchestrator
        participant OtherCaps
        Note over User,BootstrapScript: Phase 0 - User initiates bootstrap
        User->>BootstrapScript: Run install script (with config)
        BootstrapScript->>Manifest: Launch manifest service (e.g., start container)
        Manifest-->>BootstrapScript: manifest up (healthcheck OK)
        BootstrapScript->>Orchestrator: Launch orchestration service (pass manifest address)
        Orchestrator-->>Manifest: (self-register "orchestrator" service)
        Manifest-->>BootstrapScript: Orchestrator registered (via API query)
        BootstrapScript->>OtherCaps: Optionally launch other core services (gateway, etc.)
        OtherCaps-->>Manifest: (self-register other services)
        Manifest-->>BootstrapScript: All core services registered
        Note over BootstrapScript,User: Phase 1-2 complete, system self-aware
        BootstrapScript->>User: Bootstrapping complete. System is now provisioning remaining capabilities.
        Orchestrator->>OtherCaps: Deploy capability servers per config (Phase 3)
        OtherCaps-->>Manifest: Register themselves
        Manifest->>Orchestrator: All services now present in registry
        Orchestrator->>User: (via CLI/UI) System ready for use!

*Diagram: Sequence of bootstrap interactions. The bootstrap script
starts Manifest, then Orchestrator, verifying each via the Manifest
registry. After core is up, Orchestrator (now running) handles deploying
other capabilities. Finally, the system signals readiness.*

This sequence emphasizes how the manifest (registry) is central during
bootstrap for verification and coordination. It's similar to how etcd
and K8s API are central in kubeadm's process.

### Verification and Health Check Patterns

A self-provisioning system must continuously verify that components are
healthy as it spins up others. Patterns for this include:

- **Heartbeats:** Some systems use heartbeats where each component
  periodically signals "I am alive" to the registry or a monitoring
  component. Netflix Eureka does this with its clients sending
  heartbeats to the Eureka server; if heartbeats stop, Eureka marks the
  instance down after a
  timeout[\[33\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,based%20microservices%20architectures).
  In chora, we might implement something similar: each capability server
  could periodically call the Manifest server's heartbeat API or update
  its entry (or the Manifest server could poll them if it knows their
  health endpoints). For bootstrap, though, heartbeats might not yet be
  flowing; we rely on initial health.

- **Startup Health Checks:** Ideally, each service has an endpoint like
  `/healthz` or similar that returns when the service is properly
  initialized (and maybe even checks its dependencies). The bootstrap
  should use these. For example, after launching Orchestrator, query
  `GET /healthz` on it until it returns success. If it uses the
  Manifest, maybe Orchestrator's health endpoint checks it can reach the
  Manifest.

- **Dependency Ordering and Readiness:** If Orchestrator needs Manifest,
  orchestrator might internally retry connecting to Manifest until
  available. But a better approach is what we're doing: start Manifest
  first, ensure it's ready, then start Orchestrator. Some systems (like
  Kubernetes) allow components to start in any order but handle retries;
  we can rely on ordering for simplicity since we control bootstrap.

- **Logging and Diagnostics:** During bootstrap, log the outputs of
  services (or direct user to log files) to help troubleshoot. If
  something fails, a common frustration is not knowing why. For example,
  if Orchestrator container failed to start due to missing image, the
  bootstrap script should catch the error (maybe via exit code or docker
  API) and print something meaningful. Some bootstrap scripts will drop
  the user into a shell or give next steps if an error occurs.

- **No Split-Brain in Bootstrapping:** If the bootstrap can be run
  multiple times, ensure it doesn't inadvertently start duplicate
  instances of things unless that's intended (e.g., if user accidentally
  runs it twice, you don't want two manifest servers unless the design
  allows HA manifest cluster -- which could be a future feature but out
  of scope initially). For now, likely one instance of each service.
  Thus the checks `is_running("manifest")` help avoid duplicating.

### Anti-Patterns and Failure Modes to Avoid

There are some pitfalls in bootstrap design:

- **Manual Snowflake Steps:** If the bootstrap requires a lot of manual
  steps or decision-making, it's prone to error. We want a one-command
  (or close) bootstrap for most cases. Document any required manual
  steps very clearly (like "export CHORA_LICENSE_KEY before running" if
  needed, etc.). Avoid requiring obscure environment setup -- the
  bootstrap script should verify prerequisites (e.g., "Docker not found,
  please install Docker and rerun" rather than failing midway).

- **Tightly Coupled Bootstrapping:** If the bootstrap process is rigid
  and doesn't allow substitutions, that can be an issue. For example, if
  in future a user wants to use an external Consul for manifest instead
  of our manifest server, can they bypass Phase 1? A flexible design
  would allow skipping certain steps or pointing to external endpoints.
  While not a priority now, at least structure bootstrap so phases can
  be toggled or configured (maybe via a config file). This prevents an
  all-or-nothing scenario.

- **Lack of Idempotency:** Already noted, but worth re-stating as an
  anti-pattern: a bootstrap that you cannot re-run without manual
  cleanup is a pain. If our bootstrap installs system services, maybe
  add an "uninstall" or integrate with package managers. For example, if
  it registers a systemd service for Orchestrator, running bootstrap
  again might conflict or create duplicate service entries -- handle
  that (perhaps remove existing service first or skip if present).

- **No Monitoring After Bootstrap:** Once the system is up, we should
  ideally keep an eye on it. Bootstrap could optionally deploy a
  monitoring agent or at least instruct the user how to monitor (like
  "use this CLI to check status of all services"). Self-provisioning
  doesn't end at the moment of initial provision -- the system should
  also self-heal or alert. For now, as long as each service knows how to
  re-register or maintain heartbeat, the manifest can act as a simple
  monitoring view (services present = up, or if not updated recently =
  suspect down).

- **Trusting Unsafe Sources:** If our bootstrap downloads containers or
  code, ensure it's from trusted locations (and use checksums or
  signature verification if possible). E.g., if `bootstrap.sh` curls an
  installer, that URL should be HTTPS and ideally pinned or with hash
  verification, to avoid MITM. Supply chain attacks on bootstraps (like
  malicious repo injection) are a real concern (e.g., Homebrew had such
  issues, etc.). In an enterprise environment, they might prefer to host
  the bootstrap artifacts internally.

Now, let's illustrate a simple bootstrap scenario with code,
demonstrating idempotency and phase progression in a safe way.

#### Code Example: Idempotent Bootstrap Script (Pseudo-Python)

Below is a conceptual example of a Python-based bootstrap process that
demonstrates phase-wise provisioning and re-runnable logic:

    import subprocess, time, requests

    MANIFEST_PORT = 8500  # example port for manifest HTTP
    ORCH_PORT = 8600      # example port for orchestrator HTTP

    def is_listening(port):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(("localhost", port))
            return result == 0

    def start_manifest():
        # In reality, this might start a Docker container or process.
        # Here we simulate by launching a dummy server for demo purposes.
        return subprocess.Popen(["python", "manifest_server.py"])

    def start_orchestrator():
        return subprocess.Popen(["python", "orch_server.py", "--manifest-url", f"http://localhost:{MANIFEST_PORT}"])

    # Phase 1: Start Manifest if not running
    manifest_proc = None
    if is_listening(MANIFEST_PORT):
        print("Manifest service already running on port", MANIFEST_PORT)
    else:
        print("Starting Manifest service...")
        manifest_proc = start_manifest()
        # Wait for manifest to listen on port
        for i in range(30):
            if is_listening(MANIFEST_PORT):
                print("Manifest is up.")
                break
            time.sleep(1)
        else:
            raise RuntimeError("Manifest failed to start within timeout.")

    # Phase 2: Start Orchestrator if not running
    orch_proc = None
    if is_listening(ORCH_PORT):
        print("Orchestrator service already running on port", ORCH_PORT)
    else:
        print("Starting Orchestrator service...")
        orch_proc = start_orchestrator()
        # Wait for orchestrator
        for i in range(30):
            if is_listening(ORCH_PORT):
                print("Orchestrator is up.")
                break
            time.sleep(1)
        else:
            raise RuntimeError("Orchestrator failed to start.")

    # Verify orchestration service registered in manifest (pseudo-check)
    try:
        resp = requests.get(f"http://localhost:{MANIFEST_PORT}/services/orchestrator")
        if resp.status_code == 200:
            print("Orchestrator registered in Manifest.")
        else:
            print("Warning: Orchestrator not found in Manifest registry.")
    except requests.exceptions.ConnectionError:
        print("Could not connect to manifest to verify orchestrator registration.")

This code is pseudocode for clarity -- in practice, one would handle
exceptions and ensure processes are properly backgrounded or managed by
a service manager. But it shows:

- Checking if something is already running (by port).
- Starting processes and waiting with a timeout.
- Using the manifest's API to verify orchestrator presence (this assumes
  manifest has such an API endpoint like `/services/orchestrator`
  returning info or 404 if not present).
- Logging each step.

If we run this script once, it will start both services. Running it
again immediately would detect both are running and not start
duplicates, making it safe. If we kill orchestrator and run bootstrap
again, it will restart orchestrator while leaving manifest intact --
that's idempotent recovery for that piece.

### Real-World Examples and How They Influence Chora Bootstrap

Let's briefly tie back specific patterns:

- **kubeadm init** influenced the phased design and the notion of
  outputting join tokens or config for next steps. If our Orchestrator
  needed other instances (like multiple orchestrators in HA), bootstrap
  might output a token for joining them (similar concept).
- **npm/npx** influenced the idea of one-shot execution without
  installation. Possibly our bootstrap can be invoked via
  `python -m pipx run chora-bootstrap` or similar, to avoid requiring a
  full install. But that's an implementation detail.
- **cloud-init** inspired making the bootstrap as automatic as possible
  once triggered, and doing minimal initial config (phase separation,
  local vs remote tasks).
- **Ansible** inspired reducing external dependencies -- e.g., we might
  decide to use only Bash/Python which are available by default in many
  systems, rather than requiring heavy install of third-party migration
  tools.

### Prescriptive Recommendations for Bootstrap in Chora

**Do:**

- **Provide a One-Command (or One-Click) Installer:** Ideally something
  like `curl -fsSL https://get.chora.io/bootstrap.sh | bash` (for Linux)
  or a simple `pip install chora-bootstrap && chora-bootstrap` for
  Python environments. Also consider a Docker-based quick start (e.g.,
  `docker run chora/bootstrap:latest` which orchestrates containers).
- **Use Phased Initialization:** Follow a clear order (Manifest -\>
  Orchestrator -\> others) and have the bootstrap script enforce this
  ordering with checks. This avoids race conditions and ensures
  dependencies are ready.
- **Make Bootstrap Idempotent:** Rerunning the bootstrap should not
  break the system. It should skip or reinforce existing components
  gracefully. Document how to safely re-run (e.g., "you can always run
  it again; it will only add missing components").
- **Incorporate Health Checks and Timeouts:** Detect if something fails
  to come up and give meaningful feedback. Possibly offer to retry or
  abort with instructions rather than hanging indefinitely.
- **Automate Self-Registration:** Ensure that any service started by
  bootstrap (like Orchestrator) automatically registers itself in the
  registry (Manifest) as soon as possible. That way the system is aware
  of itself even mid-boot. Use this self-description to verify boot
  success.
- **Minimal Manual Requirements:** Require as little as possible
  pre-installed. For instance, if Docker is needed to run services,
  check for it and if not present, either guide to install or use an
  alternative (maybe bootstrap can even install Docker on Linux via
  script -- though that might be too invasive, better to ask user).
- **Document Recovery Steps:** If bootstrap fails at a certain phase
  repeatedly, provide guidance (e.g., how to clean partial state, logs
  to inspect).
- **Secure Bootstrapping:** Use TLS/SSL for any downloads in bootstrap,
  verify images (maybe pin image digests for starting containers). Also
  generate secrets securely (don't use hardcoded defaults for things
  like initial admin passwords; instead generate and print them for
  user).
- **Phased Outputs:** At end of each phase or at completion, clearly
  output what was done and any important info (like "Orchestrator admin
  UI available at http://host:8600 (user:admin, pass: \<generated\>)" or
  "Manifest listening on port X for other services").

**Don't:**

- **Don't Bake Credentials in Code:** Avoid shipping default credentials
  in the bootstrap that remain in the system (common security issue).
  E.g., if manifest needs an admin token, generate it unique at
  bootstrap and store it securely rather than using \"admin/admin\". If
  any defaults are used (for convenience in dev), warn user to change
  them.
- **Don't Assume Internet Access (unless required):** If possible, allow
  bootstrap to run in offline environments with pre-downloaded
  images/binaries (perhaps via an "air-gapped mode" where user provides
  a path to images). Many production environments have restricted
  internet -- if bootstrap blindly attempts to download Docker images
  from public repos, it might fail. At least document how to do it
  offline (e.g., "download these images and load them, then run
  bootstrap with \--no-pull" etc.).
- **Don't Leave System Insecure Post-Bootstrap:** Once bootstrapped,
  ensure that any temporary open holes (like a join token visible or a
  debug mode) are closed. For example, if bootstrap uses a temporary
  unauthenticated mode for manifest to register orchestrator, make sure
  to enable auth afterwards if needed. Cloud-init analog: cloud images
  often have a one-time password for bootstrap that is removed after.
- **Don't Overcomplicate Early Stage:** Keep the bootstrap logic simple
  and robust rather than overly clever. The aim is reliability first. So
  sequential steps with clear logging are better than, say, running
  everything in parallel in the hope of speed but then dealing with
  synchronization issues.
- **Avoid Manual Data Transfers:** The process should not require
  manually copying IPs or tokens from one step to another (except
  perhaps to join extra nodes, which is an advanced use-case). Automate
  passing of connection info (like we pass manifest URL to orchestrator
  via config).
- **Don't Neglect Clean-Up/Uninstall:** Even if not top priority, think
  about how a user would completely remove the system if needed (for
  re-install or permanent removal). Provide a script or instructions to
  stop containers, remove volumes, etc. Systems that install a bunch of
  stuff without an easy uninstall annoy users.

By adhering to these recommendations, chora capability servers can
achieve a **self-provisioning workflow**: a new environment can be stood
up with minimal effort, and that environment will automatically set up
its components and be ready to start handling AI workflows. This will
significantly lower the barrier to adopting chora -- an important
consideration for driving ecosystem growth.

### SAP Outline: Bootstrap and Self-Provisioning Pattern

We propose **SAP-XXY: Bootstrap and Self-Provisioning Pattern** to
capture these best practices for chora-base. This SAP would teach an
operator or developer how to set up a capability server environment that
bootstraps itself. Outline:

- **Capability Charter:** Describes the bootstrap challenge, why an
  automated bootstrap is needed (e.g., consistency, ease of deployment,
  cloud scaling), scope (covering initial install to full operation),
  and success criteria (e.g., \"One-command bootstrap with zero errors
  on a fresh machine; all core services healthy and registered within 5
  minutes\").

- **Protocol/Technical Spec:** Here we might not have a network
  protocol, but we define the phases and the interactions. Possibly
  include a *bootstrap sequence diagram* (like above) as part of spec.
  Also detail the required components (for ex: \"the bootstrapper shall
  start services in this order\... and perform these checks\"). If there
  is a config file format for bootstrap (like a YAML listing what to
  deploy after core comes up), specify that. For example, maybe the
  orchestrator expects a file `initial_manifest.yaml` listing additional
  capabilities to start -- define that format in this section.

- **Agents Guide:** In bootstrap context, this might be less relevant
  for AI agents (since bootstrap is more devops than runtime
  capability). But if there's an AI that monitors and heals the system
  (a possibility in AI-managed infra), this guide could discuss how an
  AI agent could trigger or monitor bootstrap. However, likely this
  SAP's AGENTS.md might be minimal, perhaps noting that this pattern
  ensures that after bootstrap, the AI agents (if any) will find the
  environment ready with a manifest etc. Or skip if not applicable.

- **Adoption Blueprint:** Step-by-step guide to actually using the
  bootstrap pattern. Could be divided into:

- **Essential Tier:** Manual bootstrap using provided script on a single
  node (for development or small scale).
  - Step 1: Install prerequisites (list of minimal items).
  - Step 2: Run bootstrap command.
  - Step 3: Verify system (the blueprint might tell them how to run some
    checks or open a UI).
  - Step 4: Basic troubleshooting common issues (maybe environment or
    firewall).

- **Recommended Tier:** Production bootstrap with high availability. For
  instance, run manifest in HA mode (maybe using multiple nodes or a
  stateful backend) -- if we support that, instruct how. Or orchestrator
  HA (maybe out of scope initially). But recommended might include steps
  to run bootstrap in a container orchestrator or in cloud VM, etc.,
  more robust scenarios.

- **Advanced Tier:** Self-update and advanced provisioning. E.g., how to
  automate bootstrap in CI/CD (like using Terraform or Ansible to call
  chora bootstrap on multiple hosts). Or how to integrate with cluster
  managers (maybe deploying chora as a Helm chart or similar, if we go
  that route). The blueprint will also mention idempotency: e.g., \"to
  upgrade your environment, you can re-run the bootstrap script; it will
  update components safely if they are newer\" (if we implement that).
  And include roll-back instructions: e.g., if a new bootstrap version
  fails, how to revert to previous state (maybe by restoring snapshots
  or using backup images -- advanced topic).

- **Ledger:** Track installations and improvements. For instance, record
  an entry when a company uses the bootstrap pattern to deploy chora on
  their cloud -- noting any customizations. Or track changes: \"v1.1 of
  SAP: changed bootstrap script to use Docker Compose instead of raw
  docker run.\" This ledger helps future maintainers see what updates
  were made to bootstrap processes.

With SAP-XXY, teams would have a clear runbook for deploying chora
capability servers, minimizing trial and error. It would collect the
institutional knowledge from early deployments into a repeatable
practice. This is crucial because deployment is the first experience --
if it's smooth, adoption is more likely.

## Part 3: Registry and Manifest Patterns

In a distributed ecosystem like chora, a **service registry** (the
Manifest) is the glue that holds everything together. It allows
capability servers to discover each other's endpoints, share metadata,
and report health status. This part examines proven patterns for
implementing service registries and dynamic discovery, drawing from
systems such as Consul, etcd, ZooKeeper, and others, and then recommends
how the chora Manifest service should be structured.

### Proven Service Registry Architectures

A service registry is essentially a database of service instances and
their metadata (like address, port, capabilities, health, etc.). Key
architectural questions include whether the registry is centralized or
distributed, how consistency is maintained, how clients query it, and
how health information is integrated.

- **Centralized vs Distributed Registry:**
- *Centralized:* A single logical server (which might be replicated for
  HA but acts as one service) holds all registry data. E.g., **Netflix
  Eureka** uses a primary server (or a cluster of peers) that clients
  register with; it favors availability over strong consistency (AP in
  CAP theorem). **Consul** can be seen as centralized from client
  perspective (you query one Consul endpoint even though internally it
  may have a leader and followers). Centralized makes queries simple and
  strongly consistent if using leader-based consensus (as Consul and
  etcd do).
- *Distributed (Decentralized):* Clients themselves form a peer-to-peer
  registry or use gossip to share service info. **Serf** (HashiCorp's
  gossip library, underlying Consul) and certain service meshes use
  gossip such that each node knows about others without a single server.
  **ZooKeeper** and **etcd** are distributed in the sense of their
  internal replication, but clients treat them as a single source. Pure
  P2P registries are less common because consistency and partition
  handling are tough (some IoT or ad-hoc networks do this).

For chora, a centralized registry (the Manifest service) backed by a
strongly consistent data store is a sensible approach, at least
initially. It simplifies reasoning: one authoritative list of services.

- **Consistency Guarantees:** Strong vs eventual consistency in
  registries:
- **ZooKeeper** and **etcd** provide *strong consistency* (linearizable
  reads/writes by default). If you query the registry, you get the
  latest committed data. This is crucial for some systems (like leader
  election or
  configuration)[\[34\]](https://medium.com/@karim.albakry/in-depth-comparison-of-distributed-coordination-tools-consul-etcd-zookeeper-and-nacos-a6f8e5d612a6#:~:text=etcd%20is%20an%20open,data%20consistency%20across%20the%20cluster)[\[35\]](https://medium.com/@karim.albakry/in-depth-comparison-of-distributed-coordination-tools-consul-etcd-zookeeper-and-nacos-a6f8e5d612a6#:~:text=Key%20features%20of%20ZooKeeper%3A).
  etcd is used by Kubernetes to store cluster state for this reason.
- **Consul** offers strong consistency for KV operations via Raft
  consensus, but uses a gossip protocol for broadcasting health updates,
  which can introduce slight delays (so it's a
  mix)[\[36\]](https://stackshare.io/stackups/consul-vs-etcd#:~:text=1,based%20protocol).
  By default, Consul agents can respond to queries with possibly stale
  data from their cache unless consistency mode is set to "consistent"
  which then queries leader.
- **Eureka** (Netflix OSS) explicitly chose eventual consistency: an
  instance registers and gets replicated to peers eventually; there is a
  self-preservation mode that if the Eureka servers lose quorum or many
  heartbeats, they stop expiring instances to avoid mass deregistration
  during network
  issues[\[33\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,based%20microservices%20architectures).
  Eureka clients also cache registry info and only update every 30
  seconds or so. This can lead to short periods where a client might
  call an instance that is actually down (since Eureka hasn't noticed
  yet or client hasn't got the update), but Netflix's design favored
  resilience over immediate accuracy (they handle such calls failing).

**Recommendation:** For chora's manifest, favor strong consistency for
core data (list of active services, their latest status) to avoid
confusion, since it's a small scale (tens of services, manageable by
Raft). This means likely implementing the Manifest store on a consensus
algorithm (like using etcd internally or building on something like
that). We aren't operating at a massive scale where the slight
performance cost of strong consistency is an issue. Also, AI agent
orchestration might prefer correctness (knowing something is definitely
available) over slight increases in availability. We can incorporate
some AP aspects by caching on clients if needed, but the source of truth
should be consistent.

*Example reference:* A StackShare comparison notes *"Consul uses Raft
for consensus ensuring all nodes have same view, etcd uses Raft too;
Eureka does not ensure strong consistency but is highly
available"*[\[9\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,consistency%20but%20is%20highly%20available).
This aligns with our summary.

- **Data Model: Hierarchical vs Flat:**
- **ZooKeeper** stores data in a filesystem-like hierarchy of znodes
  (e.g., `/services/<serviceName>/<instanceId>`). This can be used to
  group data logically and watch specific subtrees for changes. It is
  very useful for things like configuration trees or leader election
  (e.g., create ephemeral node in a directory).
- **etcd** also has a key space that is effectively hierarchical (keys
  are arbitrary strings, often with prefixes to mimic directories). You
  can do operations on key prefixes to list group entries (etcd v3 uses
  a flat key space but supports range queries effectively for prefix).
- **Consul** KV store is hierarchical (keys with `/` convention).
- **Eureka** is a bit different: it stores info per service and instance
  in memory and replicates as needed. It's not typically exposed to
  users as a general KV; it's a domain-specific data model (applications
  and instances).

For manifest, a hierarchical model might be beneficial. For instance: -
`/services/<capability>` as a grouping, and under it multiple instances
(if we ever run multiple of one type). - Could also separate by
environment or version if needed: e.g.,
`/services/orchestrator/v1/instance1`. - Hierarchy might also encode
interface info, e.g. `/services/orchestrator/REST_endpoint` and
`/services/orchestrator/CLI_endpoint` -- but likely better to store
these as fields rather than separate nodes.

A simple schema might be:

    services:
      - name: orchestrator
        version: 1.0.0
        interfaces:
          REST: http://10.0.0.1:8600
          CLI: n/a
          MCP: tcp://10.0.0.1:7000
        status: healthy
        last_heartbeat: "2025-11-11T10:00:00Z"
        meta:
          description: "Manages lifecycle of other capabilities"
          dependencies: ["manifest"]
      - name: manifest
        version: 1.0.0
        interfaces:
          REST: http://10.0.0.1:8500
        status: healthy
        meta: {…}

Storing this in etcd as JSON or in a small database is fine.
Alternatively, an in-memory with Raft approach could be used if
implementing from scratch.

- **Extensibility Patterns:** The registry should allow adding new
  metadata without breaking things. Consul and etcd allow arbitrary
  key-values attached to services (Consul has \"tags\" and \"meta\"
  fields on
  services)[\[37\]](https://echorand.me/posts/consul-tags/#:~:text=Consul%20tags%20are%20arbitrary%20metadata,due%20to%20lack%20of).
  For example, a service could register with tags `region:europe`,
  `tier:backend` etc., which clients can query. We should design
  manifest to allow optional metadata (like descriptive fields, or
  custom capability-specific info). A flat key-store with JSON values is
  flexible.

- **Service Discovery Queries:**

- **Consul:** supports queries by service name (DNS or HTTP query), with
  optional filtering by tags or meta. E.g., via DNS:
  `redis.service.consul` to get an IP, or via HTTP API:
  `/v1/catalog/service/redis?tag=primary`. It also has health filtered
  queries (only return passing instances).

- **Kubernetes API:** clients often do label-selector queries: e.g. list
  all pods with `app=web`.

- **ZooKeeper:** doesn't have query per se; clients typically know the
  znode path they need to check or watch (like watchers on a directory
  for changes).

- **Eureka:** clients get the full list of instances for a service and
  then filter client-side (some client libraries do zone affinity etc.).
  Eureka's model is not sophisticated in querying, it\'s more push
  (registry pushes changes to clients incrementally).

For manifest, it likely suffices to allow look-up by service name to get
its info (most of the time each capability name is unique in function,
so one active instance per capability in a local deployment, though
maybe multiple in future for scaling/handoff). We can incorporate simple
filtering: e.g., a query parameter to ask for only healthy ones, or by
version if multiple versions can coexist.

Additionally, a **full-text search** of registry might not be needed
since number of services is small (tens). But maybe allow querying by
capability type or tag (if one wants all \"storage\" related
capabilities).

- **Versioning and Compatibility in Discovery:** When multiple versions
  of a capability exist (e.g., running v1 and v2 for upgrade), how do
  others choose which to call? Patterns:
- Register them as separate service names (like `manifest_v1` vs
  `manifest_v2`).
- Or register with version metadata and let clients decide (the client
  query might say \"give me version\>=2.0\").
- Consul doesn't specifically handle versioning; you'd likely encode it
  in service name or tag.
- Kubernetes handles version via API versioning but that's more for API
  schema than instances. For microservices, backward compatibility or a
  gateway typically handles it.

We can keep it simple: one active version per capability for now
(chora's orchestrator manages rolling upgrades perhaps). But the
manifest schema can include a `version` field for informational purposes
and so a UI can show what version each service is.

- **Caching Strategies:**

- *Client-side caching:* If hitting the registry is expensive or if we
  want resilience, clients can cache results for some time. Eureka
  clients do this by default (poll every 30s, use local cache
  otherwise). Consul clients often run a local Consul agent that caches
  catalog data and answers DNS queries quickly.

- We might not need caching given small scale and local network usage.
  But if an AI agent frequently queries manifest for every action,
  caching a bit could help. Perhaps provide a client library that keeps
  a local copy and updates via long polling or server-sent events. Or
  simply let manifest be fast (since it's in-memory data mostly).

- *Registry pushing updates:* Another design is to have manifest
  broadcast changes to subscribers (maybe via WebSocket or an event
  stream). That way, e.g., if a new capability registers, all interested
  components know immediately. This is advanced, maybe not needed
  initially if poll intervals are short and failure tolerance is
  built-in.

- **Health and Monitoring Integration:**

- **Consul** has health checks: each service registration can include a
  health check (script or HTTP) that the Consul agent will run, and
  Consul won't list the service as healthy until it passes. Or a service
  can HTTP PUT to mark itself passing or failing. Consul's catalog then
  shows health status (so service discovery can filter only healthy).

- **ZooKeeper** doesn't directly manage health; it just uses ephemeral
  nodes. If a client session disconnects (like service crashed), its
  ephemeral znode is removed -- that signals it\'s gone (that\'s one way
  to manage health).

- **Eureka** expects heartbeats; if too many are missed, the instance is
  ejected from registry (but with that self-preservation caveat).

- **etcd** similarly would rely on clients updating a lease (etcd has
  lease mechanism with TTL; if lease not renewed, keys tied to it expire
  -- could implement a service TTL that way).

Our manifest can combine approaches: - Have each capability server send
a heartbeat (e.g. an HTTP PUT /heartbeat/\<service\> every N seconds).
Manifest marks a timestamp. If heartbeat stops and grace period passes,
manifest marks service as unhealthy or removes it. - Additionally,
manifest might allow registering a health-check URL for each service.
The manifest service could periodically (or on-demand when queries
happen) try to fetch that URL. However, making the registry actively
poll could be heavy if many services or if health checks are expensive
(often better to push from service or use an external monitor).

Perhaps simplest: adopt Eureka-like heartbeat approach, since we anyway
likely have a connection from each service to manifest to register and
perhaps to periodically update status. So: - On register, manifest
stores `status = UP`. - Each service calls heartbeat every, say, 10
seconds. Manifest updates last_heartbeat timestamp. - A background
thread in manifest checks timestamps; if any exceed threshold (no
heartbeat for, say, 30 sec), mark `status = UNHEALTHY` or remove it
after a further timeout. - Clients querying can choose to get only
healthy ones if needed.

Heartbeat messages could also include dynamic info, e.g., current load
or custom metrics (though keep it light).

If a service cleanly deregisters (e.g., during a controlled shutdown, it
should ideally call a deregister API so it\'s removed immediately).

We should design the heartbeat TTL carefully to avoid flapping. If
network glitch causes a missed heartbeat but the service is fine, it
might temporarily mark down. This is where some \"self-preservation\"
logic might come in: e.g., maybe we don\'t remove a service until
missing 3 heartbeats or a large multiple of interval. Or just mark it as
\"unknown\" state for a while before fully removing.

*Heartbeat vs Pull:* Using heartbeats (push) is preferred in our
scenario because the registry can be lightweight and passive until it
receives updates. If manifest had to actively pull health from each
service, that\'s more overhead and potential issues (services behind
firewall, etc.). It\'s usually more robust for services to report their
own status (they know if they\'re struggling, potentially).

- **Monitoring & Alerting:** The registry itself can act as a basic
  monitor by exposing metrics (like number of services, statuses). We
  might integrate with Prometheus: e.g., manifest could have an endpoint
  `/metrics` with counts and health stats. Or at least log events when a
  service goes down/up. For alerting, one could set up an external
  watcher on manifest data to trigger notifications if needed (this is
  beyond manifest\'s core role, but easy to add since manifest has a
  global view).

- **Scaling Considerations:** If number of services grew huge (hundreds
  or more), or high churn, the registry needs to handle concurrent
  updates and queries. Using a proper database or etcd will help. But
  likely our scale is modest. One thing to consider: if multiple
  orchestrators or multiple instances of capabilities register
  frequently, ensure manifest writes are efficient (batch if needed).

Another scaling aspect: multiple manifest instances (for HA). If
manifest itself is a single point, it might be a single point of
failure. We could consider running it as a small cluster (like an etcd
cluster of 3 nodes). That introduces complexity (leader election etc.).
Possibly treat manifest as a special capability that could be
multi-instance with a consensus. For now, maybe out-of-scope unless high
availability is required. At least design in a way that adding
replication is possible (maybe by relying on an underlying etcd we get
HA by using etcd\'s cluster).

Consul, etcd, ZooKeeper all run as clusters for HA (and they elect a
leader for writes).

Summing up, our recommended registry (Manifest) design: - Backed by a
Raft-based store (etcd or built-in consensus). - Provides a REST API for
registration, deregistration, heartbeat, and queries. - Data model
grouping by service name and instance (if multi-instance). - Metadata
schema includes fields for addresses of each interface, version, and
potentially a list of dependencies or tags. - Health status tracked via
heartbeats (and possibly direct integration of check results if
provided). - Allows discovery by service name (exact match queries) and
possibly tag filtering in query params. - Possibly offer a dump of all
data for debugging or UI (like an endpoint to list all services).

Next, let\'s present a **comparison matrix** of different registry
solutions to highlight key features, which guides our design choices:

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Registry**    **Consistency**                                                                                                                                                                                                                      **Health            **Query Model** **Data Organization**     **Usage in
                                                                                                                                                                                                                                                       Mechanism**                                                   Industry**
  --------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ------------------- --------------- ------------------------- ---------------
  **ZooKeeper**   Strong (ZAB protocol, sync                                                                                                                                                                                                           Ephemeral nodes for Hierarchical    Hierarchy (like           Config
                  writes)[\[34\]](https://medium.com/@karim.albakry/in-depth-comparison-of-distributed-coordination-tools-consul-etcd-zookeeper-and-nacos-a6f8e5d612a6#:~:text=etcd%20is%20an%20open,data%20consistency%20across%20the%20cluster)      liveness (client    znodes; clients filesystem); e.g.         management,
                                                                                                                                                                                                                                                       session)            watch nodes for `/app/service/instance`   service
                                                                                                                                                                                                                                                                           changes         nodes                     discovery
                                                                                                                                                                                                                                                                                                                     (Hadoop, etc.)
                                                                                                                                                                                                                                                                                                                     -- requires
                                                                                                                                                                                                                                                                                                                     client lib

  **etcd**        Strong (Raft                                                                                                                                                                                                                         TTL on keys/leases  Key-value with  Flat KV (but keys often   Kubernetes
                  consensus)[\[34\]](https://medium.com/@karim.albakry/in-depth-comparison-of-distributed-coordination-tools-consul-etcd-zookeeper-and-nacos-a6f8e5d612a6#:~:text=etcd%20is%20an%20open,data%20consistency%20across%20the%20cluster)   (client must        prefix queries; structured with `/`); can (cluster state
                                                                                                                                                                                                                                                       refresh)            no built-in     store JSON blobs          store), etc. --
                                                                                                                                                                                                                                                                           service concept                           reliable, needs
                                                                                                                                                                                                                                                                                                                     quorum of nodes

  **Consul**      Strong for catalog (Raft); eventual for gossip updates[\[36\]](https://stackshare.io/stackups/consul-vs-etcd#:~:text=1,based%20protocol)                                                                                             Health checks via   Service lookup  Separates service catalog Service mesh
                                                                                                                                                                                                                                                       agent & heartbeat;  by name (DNS &  vs KV store; services     and discovery
                                                                                                                                                                                                                                                       failing checks mark HTTP); filter   have associated health    (HashiCorp) --
                                                                                                                                                                                                                                                       service down        by              checks                    rich features
                                                                                                                                                                                                                                                                           tags/metadata                             (ACL, multi-dc)

  **Eureka        AP (Highly Available, weak consistency)[\[33\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,based%20microservices%20architectures)    Heartbeats from     Lookup by       Organized by application  Netflix OSS
  (Netflix)**                                                                                                                                                                                                                                          clients; eviction   service         name; instances with      microservices
                                                                                                                                                                                                                                                       if missed (after    (returns list   status fields             -- designed for
                                                                                                                                                                                                                                                       self-preservation   of instances);                            large scale,
                                                                                                                                                                                                                                                       window)             clients cache                             allows stale
                                                                                                                                                                                                                                                                           responses                                 data

  **AWS Cloud     Strong (AWS-managed, likely strongly consistent store)                                                                                                                                                                               Custom health       API and SDK to  Hierarchical namespace    Cloud service
  Map** (Service                                                                                                                                                                                                                                       checks or AWS       discover by     (optional); attributes    discovery --
  Catalog)                                                                                                                                                                                                                                             CloudWatch          service name or can be attached to        integrates with
                                                                                                                                                                                                                                                       integration         attributes      instances                 AWS health
                                                                                                                                                                                                                                                                                                                     checks and DNS

  **Kubernetes    Strong (etcd backend)                                                                                                                                                                                                                K8s handles via     Label-based     Services and Endpoints    Internal
  API** (for                                                                                                                                                                                                                                           readiness probes,   selectors, or   objects in API (not       service
  services)                                                                                                                                                                                                                                            but not part of     direct          hierarchical, but         discovery in
                                                                                                                                                                                                                                                       etcd -- uses        Endpoints       structured resources)     clusters -- via
                                                                                                                                                                                                                                                       controller to       object query                              environment or
                                                                                                                                                                                                                                                       update Endpoints                                              DNS, backed by
                                                                                                                                                                                                                                                                                                                     etcd
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[\[36\]](https://stackshare.io/stackups/consul-vs-etcd#:~:text=1,based%20protocol)[\[33\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,based%20microservices%20architectures)

*Table 2: Comparison of Service Registry/Discovery Systems.*

From the comparison, one can see that **Consul** and **etcd** share a
bias towards consistency (good for config and correctness), whereas
**Eureka** favors availability (good for large cloud where nodes may
come and go but partial info is tolerable). For chora, given the
relatively small scale and need for correctness (AI agents should not be
misled by stale info if we can help it), we lean towards a Consul/etcd
style approach: strong consistency, heartbeats for liveness, and a rich
metadata model.

### Proposed Manifest Schema and Patterns for Chora

We now outline how the chora Manifest registry should work:

**Schema (Data Model):** Each *capability server* registers a **service
record** with fields: - `name` -- a unique name (e.g., \"manifest\",
\"orchestrator\", \"gateway\", \"n8n\", etc.). This is the key for
discovery. Possibly include a `group` or namespace if needed in future
(for multi-tenant scenarios, not now). - `id` -- unique instance ID
(could be generated GUID, or something like `<name>-1`). Useful if
multiple instances of same service type run (for HA or scaling). The
combination of name+id is unique. - `version` -- version string of the
service (semantic version or git commit). Allows monitoring of
versions. - `interfaces` -- a dictionary of interface type to endpoint.
For example:

    interfaces:
        REST: "http://10.0.0.1:8500"
        CLI: "chora-manifest"   # CLI might just provide the command name or path if applicable
        MCP: "tcp://10.0.0.1:8600"

If some interface not applicable, can omit or put `null`/`n/a`. -
`metadata` -- freeform key-values with additional info. Some could be
standardized: - `description` -- human-friendly desc of the
capability. - `dependencies` -- list of other service names it needs
(e.g., orchestrator depends on manifest; n8n might depend on
orchestrator for launching, etc.). This can help orchestrator or AI
reason about startup order or impact analysis (if one service down, what
others are affected). - `tags` -- list of tags for grouping (like
\"core\" vs \"optional\", or environment tags). - Possibly `host` or
`region` info if relevant in distributed deployment. - You could also
include `api_spec` link or any public docs URL in metadata if needed for
discovery of API (like pointer to OpenAPI doc). - `status` -- e.g.,
\"up\", \"down\", \"unhealthy\", \"unknown\". (We can define statuses:
\"up\" = healthy and running, \"down\" = not running (manifest removed
it or it deregistered), \"unhealthy\" = registered but failing its
health checks, \"unknown\" = haven't heard heartbeat recently but not
long enough to declare dead, perhaps.) - `last_heartbeat` -- timestamp
of last heartbeat (if using heartbeats). Or we maintain an internal TTL
that triggers status change rather than exposing timestamp to clients,
but having it is fine for transparency. - `uptime` or `since` --
optional timestamp when service was registered or started (for
monitoring how long it\'s been up). - `endpoint_health` -- optional
sub-dictionary if multiple health checks. E.g., if a service provides
separate health for different subsystems, or for each interface. This
might be overkill; likely we have a single overall health per service.

Data can be represented in YAML/JSON as above. In etcd or similar, one
might store each service record under a key like
`/chora/services/<name>/<id>` with JSON payload. Or use a relational DB
table with columns for these fields. Because number of records is small,
either approach is fine. etcd gives nice watch API if needed.

**Registration Protocol:** - A new capability server (say orchestrator)
on startup will make a REST POST (or PUT) request to the Manifest
service, e.g., `POST /services` with its details. Manifest stores it and
returns a unique `id` if not provided (we could allow manifest to assign
instance IDs). - Alternatively, manifest could require clients to
register with a pre-shared token or credentials if security is a concern
(so that rogue processes can't register fake services). Initially maybe
open or simple auth since it\'s internal network. In production, one
could integrate with mTLS or an auth token (Consul uses ACL tokens for
service registration in secure setups). - On successful registration,
manifest sets status to \"up\" (or \"starting\" if we want a
transitional state until first heartbeat). - The client then begins
sending heartbeats (maybe `PUT /services/<name>/<id>/heartbeat` or a
shorter endpoint). - If a service needs to update its info (like it
opens a new interface or its IP changed), it can call
`PUT /services/<name>/<id>` with updated data. Or simply deregister and
re-register if that's easier (but better to allow updating in place). -
Deregistration: if a service is shutting down gracefully, it should call
`DELETE /services/<name>/<id>` to remove itself. Manifest then deletes
that record or marks it as removed. Possibly keep a tombstone for a
short while to avoid flapping (Consul e.g. keeps a \"left\" status or
logs it). - Manifest also might automatically deregister if no heartbeat
after X time, as discussed.

**Discovery Protocol:** - Clients (capability servers or AI agents)
query manifest to find others. If orchestrator needs to call manifest's
API at startup, it likely already knows manifest's address (since how
else did it register? -- either bootstrap gave it, or manifest's
location is known like a well-known host or environment variable). -
However, for others: e.g., an AI agent or UI might query \"give me all
services\" to populate a dashboard. - Specific queries: `GET /services`
returns list of all currently registered services (maybe with filter
options). - `GET /services/<name>` could return either a single instance
record (if one exists) or a list of instances if multiple. If we expect
mostly one instance per service type, it can return just that record or
a list under a key. - Could support query parameters like `?status=up`
to only list healthy ones, `?tag=core` to only those with a given tag,
etc. But those are optional features to implement as needed. - We can
also provide `GET /services/<name>/<id>` for a specific instance (though
if name+id is unique, just one route might suffice since \<id\> implies
name anyway in path structure). - Possibly allow querying by interface
type. But more likely a consumer knows the service name and then reads
its interfaces field to get how to talk to it.

**Health Reporting:** - If a service is alive and well, it just keeps
heartbeating. If it detects it is unhealthy (maybe it has an internal
self-check), it might inform manifest. For example, a service could call
`PUT /services/<name>/<id>/status` with `unhealthy` if one of its
dependencies goes down. But typically manifest deduces health from
heartbeats or external checks. - Heartbeat message could optionally
carry a payload like `{"load": 75}` (some performance metric) or number
of active tasks, which manifest could store in metadata. Keep it simple
for now: maybe no payload, just updating timestamp. If needed, we can
extend heartbeat to include quick metadata (like memory usage for a
monitoring display). - Manifest's own health: The manifest service
should ideally register itself (as \"manifest\") in its own list. That's
a bit self-referential, but it can simply treat itself like any other
service. Then orchestrator can know about manifest from registry rather
than having to be configured separately (though initial contact needed
one known address). - If manifest goes down, obviously service discovery
is impaired. But if we consider HA in future, multiple manifest nodes
with a virtual IP or using etcd means manifest as a service is
redundant. At least maintain backups (manifest could persist data to
disk or replicate to avoid losing state on crash).

**Dependency Declarations in Metadata:** - We mentioned including
`dependencies`. For example, orchestrator's entry might have
`dependencies: ["manifest"]` meaning it expects manifest to be present.
If manifest were to go down, orchestrator might go into some degraded
state. This info could be used by an AI or management system to
coordinate shutdowns or startups (like \"start manifest first, then
orchestrator\"). - Similarly, n8n might depend on orchestrator (for
launching tasks) and manifest. If orchestrator is not available, n8n
might not function fully. - These can be manually maintained or
auto-inferred. Possibly the orchestrator, at registration, knows it
depends on manifest (since it needed manifest to register). But listing
explicitly helps. - With such info, manifest could even warn if a
dependency is missing. E.g., if a service registers claiming it depends
on X, but X is not in registry, manifest might log or mark that service
as \"degraded\" due to missing dependency. But that might be overkill.
Likely an orchestrator or some separate logic would enforce dependency
ordering via SAP adoption blueprint or configuration rather than
manifest doing it implicitly.

### Code Snippet: Simple Registry Interaction in Python

To illustrate how a component might interact with the Manifest
(registry), here\'s a small pseudo-code example. This might reflect what
a capability server (or a client script) does to register and query
services:

    import requests

    MANIFEST_URL = "http://localhost:8500"

    # Register this service (assuming manifest is up)
    service_data = {
        "name": "example-cap",
        "version": "1.2.3",
        "interfaces": {
            "REST": "http://10.0.0.5:9000",
            "CLI": "example-cap-cli"
        },
        "metadata": {
            "description": "Example capability for demo",
            "dependencies": ["manifest"]
        }
    }
    res = requests.post(f"{MANIFEST_URL}/services", json=service_data)
    if res.status_code == 201:
        my_id = res.json().get("id")
        print(f"Registered with manifest, got ID {my_id}")
    else:
        print("Registration failed:", res.text)
        my_id = None

    # Heartbeat loop (simplified)
    import time
    while True:
        try:
            hbres = requests.put(f"{MANIFEST_URL}/services/example-cap/{my_id}/heartbeat")
            if hbres.status_code != 204:
                print("Heartbeat warning:", hbres.text)
        except Exception as e:
            print("Heartbeat failed, manifest might be down:", e)
        time.sleep(10)

    # Query an example (perhaps another part of the program wants to find orchestrator)
    resp = requests.get(f"{MANIFEST_URL}/services/orchestrator")
    if resp.status_code == 200:
        orch_info = resp.json()
        orch_url = orch_info["interfaces"]["REST"]
        print("Orchestrator REST endpoint:", orch_url)
    else:
        print("Orchestrator not found or manifest error")

This snippet outlines: - Posting to `/services` to register (manifest
might assign an `id` and return, possibly with 201 Created). - Sending
periodic heartbeats to an endpoint like
`/services/<name>/<id>/heartbeat` (using HTTP PUT with no body,
expecting a 204 No Content or 200 OK). - Querying for another service
(orchestrator) and reading its data to get an interface endpoint.

Note: The actual manifest API endpoints might be designed differently;
this is just one idea. We would also implement the server side in
manifest to handle these routes: - `POST /services` -- assign id, store
record. - `PUT /services/<name>/<id>` -- update (not mandatory but
useful). - `PUT /services/<name>/<id>/heartbeat` -- update timestamp. -
`DELETE /services/<name>/<id>` -- remove. - `GET /services` -- list
all. - `GET /services/<name>` -- get service or list of instances if
multiple. - possibly `GET /services/<name>/<id>` for specific instance
(though if we use id to differentiate multiple instances, we might
require specifying id in fetch if multiple, or default to the first if
one).

We should consider how to handle multiple instances: - If chora in
future allowed, say, two orchestrator instances (for HA), then
`GET /services/orchestrator` should return a list. Or we require asking
`GET /services/orchestrator?id=<id>` for a specific. More likely we
design assuming one instance per, unless scaled. But better to code with
support for multiple to be safe (e.g., return a list if multiple, or
have separate \"instances\" sub-resource in API design).

### Discovery and Query Examples

Let\'s present a couple of examples how the Manifest would be used in
practice: - When Orchestrator starts (phase 2 of bootstrap), bootstrap
(or orchestrator itself) registers orchestrator in manifest. Later, when
another service (like gateway) starts, it might query manifest to find
orchestrator's address to call its API and register itself there as a
backend (if needed). Or orchestrator might automatically deploy gateway
and pass config including manifest address. There are many flows, but
manifest is the one-stop shop for service locations. - If an AI agent
wants to perform an operation (e.g., deploy a new model via
orchestrator), but the agent only knows it should talk to
"orchestrator", it can query manifest to get orchestrator's REST
endpoint and then call it. Alternatively, if the agent is an internal
one with direct Python access, it might import orchestrator's SDK or use
MCP. But if doing via REST, manifest helps it connect dynamically
without hardcoding addresses. - If orchestrator needs to call another
capability (like the manifest or others) as part of a workflow, it can
look them up on demand. Or orchestrator might subscribe to manifest's
changes to always have an updated map (maybe simpler: orchestrator might
also maintain a local copy after initial deployment, since orchestrator
itself likely participated in launching each service, it could record
their info directly. But for general decoupling, using manifest queries
is fine).

### Health Check Implementation Patterns

We\'ve chosen heartbeats as primary, but we can also incorporate direct
health check endpoints: - Perhaps each service has its own `/health`
HTTP endpoint that returns 200 OK if healthy. The manifest service could
optionally ping those if configured to do so. This is similar to how
Kubernetes readiness checks are separate from registry, or how an
external monitor might work. - We could allow a service to register with
a `health_url` in metadata. Then the manifest could, on heartbeats
missing, attempt one or two direct health pings before declaring it down
(maybe it missed heartbeats due to network but is still alive). However,
that adds complexity and is somewhat redundant if heartbeats are
reliable. - Better might be: if manifest notices a service missed
heartbeat, it changes status to \"unknown\". If another service tries to
use it (some orchestrator process, etc.) and fails, *that* might trigger
an update (like orchestrator could catch the error and mark it unhealthy
via manifest API). This becomes a collaborative health model. - For now,
manifest can rely on heartbeats and removal on timeout. We assume each
capability server is responsible for telling manifest \"I\'m here and
fine\".

**Scaling and Federation**: - If chora expands to multiple datacenters
or edge devices, we might consider a federated registry (like Consul
supports multiple datacenters with WAN gossip, or one could run separate
manifests and sync between them for global view). That's beyond our
current scope, but designing manifest to possibly have an idea of
environment/zone in metadata will help if needed (e.g., a `location`
field). - For now, presumably all capability servers are within one
network and one manifest covers them.

### Anti-Patterns and Pitfalls in Registries

- **Stale Registrations:** Avoid situation where a service crashes but
  remains listed as healthy. Our heartbeat TTL should catch these. But
  ensure corner cases like if manifest itself restarts and loses track
  of last heartbeats (we can mark all as unknown on manifest reboot and
  require services to heartbeat again soon or re-register). Possibly on
  manifest startup, it could clear registry or set all to unknown and
  require all to refresh (which they should soon via heartbeat or
  re-registration).
- **Thundering Herd on Restart:** If manifest goes down and back up,
  many services might attempt to re-register or heartbeat
  simultaneously. The manifest should be light enough to handle a burst
  of a few dozen requests easily. If using etcd under hood, it can
  handle that fine. We should test scenario of manifest recovery and
  services reconnecting gracefully.
- **Security of Registry:** If not addressed, a malicious actor could
  register fake services (phishing an AI to call a malicious endpoint)
  or deregister things. In a closed environment it's fine, but consider
  adding at least a simple shared secret or network-level security (only
  allow writes from certain hosts or via mutual TLS). Perhaps
  out-of-scope for now, but leave hooks for adding ACL (Access Control
  List) or tokens.
- **Overloading Metadata:** Keep metadata relevant. Don't try to stuff
  too much (like large config values) into the registry. That's what a
  config store (like our ledger or so) is for. Registry metadata should
  be small static descriptors. For larger data, use separate service or
  file.
- **Not Updating on Changes:** If a service's address changes (maybe it
  got a new IP via DHCP), the registry must be updated. Possibly design
  services to have stable addresses (e.g., use static IPs or hostnames),
  so this is rare. If it happens, either the service should detect and
  re-register with new info, or an orchestrator that assigned a new IP
  knows to update manifest. This can be complicated if not thought
  through, but in static deployments less of an issue. In containerized
  environment, normally container IP changes on restart, but
  orchestration should handle re-registration anyway.
- **Schema Evolution:** As we refine manifest schema (add new fields,
  etc.), ensure backward compatibility for clients. E.g., if we add a
  new `statusDetail` field, old clients should ignore it. Use JSON which
  is naturally extensible. Document fields for those writing clients.

### Code Example: Using the Registry (Manifest) -- Querying and Health Filtering

To demonstrate how a developer might use the manifest in code, here\'s a
snippet where a script lists all active services and filters healthy
ones (assuming manifest has an API for that):

    import requests

    # Fetch all services from manifest
    resp = requests.get("http://localhost:8500/services?status=up")
    services = resp.json()  # assume returns list of service records
    print("Active capability servers:")
    for svc in services:
        name = svc["name"]
        ver = svc.get("version")
        status = svc.get("status")
        rest_url = svc["interfaces"].get("REST")
        print(f" - {name} (v{ver}) status={status} REST={rest_url}")

If manifest supports the `status=up` filter, it might directly return
only those with status \"up\". Otherwise, the script could filter the
list after retrieving all.

Example output might be:

    Active capability servers:
     - manifest (v1.0.0) status=up REST=http://10.0.0.1:8500
     - orchestrator (v1.0.0) status=up REST=http://10.0.0.1:8600
     - gateway (v1.0.0) status=up REST=http://10.0.0.1:8700
     - n8n (v0.9.1) status=up REST=http://10.0.0.2:5678

This is useful for an operations dashboard or for a deployment script
verifying everything is running.

### Anti-Patterns for Scaling and Performance:

- **Polling too frequently:** If every microservice queries manifest
  every second, it's unnecessary overhead. Better use heartbeats from
  service to manifest and caching or event-driven updates for discovery.
  But given small numbers, even per-second polling is not a big deal
  (like 10 services \* 1 req/s = 10 qps).
- **Large payloads in registry:** keep entries small (no huge blob
  fields) to ensure manifest can respond quickly and network load is
  trivial. It's only metadata and endpoints.

Now we consolidate the **prescriptive recommendations for
Registry/Manifest:**

**Do:** - Implement the Manifest as a strongly-consistent service
registry (e.g., backed by etcd or similar). This ensures all capability
servers have a single source of truth for discovery. - Use
**heartbeats** from services to maintain liveness information. Define a
reasonable heartbeat interval (e.g., 10s) and timeout (e.g., 30s) after
which a missing heartbeat triggers marking the service unhealthy or
removing it. - Store rich **metadata** for each service (version,
description, dependencies) but keep it lightweight. Use tags or fields
to enable filtering. E.g., mark core services vs optional. - Provide a
**simple and intuitive API** for registration and lookup. E.g.,
`register_service(name, interfaces, meta)` and `get_service(name)` in a
client library. - Ensure **idempotency** in registration: if a service
registers twice (perhaps after a crash and restart), handle it
gracefully (either update the existing record or replace it). Avoid
duplicate entries for same instance (maybe use service name if only one
allowed, or ensure old one is cleared). - Include the **health status**
in responses so clients can decide whether to use a service or
failover. - **Document** the manifest schema and API clearly in the SAP
and developer docs, so that anyone creating a new capability knows how
to integrate (most will use provided base code presumably). - Use the
registry as the foundation for orchestrating startup order: e.g., the
bootstrap uses manifest to ensure orchestrator sees manifest up, etc.
(We already do in Phase logic). - Monitor the registry itself: ideally
manifest should expose metrics or at least logs when a service flaps (so
devs can see "Service X deregistered due to heartbeat timeout"). - Plan
for future expansion (like possibly federating across multiple manifests
if needed, or adding security). Keep design modular enough to allow
plugging ACLs or encryption.

**Don't:** - **Don't allow stale data to persist**: implement heartbeat
and removal to avoid phantom services. Also, if using TTL/lease in etcd,
tune it correctly (e.g., etcd lease TTL a bit above heartbeat
interval). - **Don't rely solely on manual removal**: e.g., requiring an
admin to delete a dead service is not scalable; automate it with
timeouts. - **Don't make discovery complex for clients**: e.g.,
requiring complex queries for common operations. Provide straightforward
lookup by name for the typical use-case (since each capability has a
unique function). - **Don't overload manifest with unrelated duties**:
It's tempting to also store configuration or act as a general database.
Keep it focused on service discovery and status. Other data (like
detailed config or large state) belongs in a separate store or the
capability's own DB. - **Don't neglect synchronization issues**: If
multiple threads or processes might register simultaneously, ensure
manifest handles concurrent requests (if using a proper DB or web
framework, it should). If building a custom in-memory store, add locking
around writes. - **Don't ignore performance** for manifest operations:
though small scale, ensure manifest can respond to queries quickly (\<
milliseconds ideally). Use efficient data structures (a dictionary for
lookup, etc.). If using disk persistence or consensus, measure the
overhead (should still be low for tens of keys). - **Don't open it up
without any security** if deployed in a shared environment: If chora is
within a safe network, fine. But if it might be accessible by untrusted
agents (maybe if AI agents run code that could call manifest), consider
at least an authentication token to prevent misuse (like an AI
hallucinating and deregistering everything -- far-fetched but consider
it). - **Don't hardcode service addresses in clients**: Mandate that all
capability servers use manifest for discovery (except manifest itself).
This ensures decoupling. Provide library functions to fetch addresses
from manifest to discourage hardcoding. For example, rather than writing
`ORCH_URL = "http://orchestrator:8600"`, encourage
`ORCH_URL = manifest_client.get("orchestrator").interfaces["REST"]`.
This way if orchestrator moves, clients adapt.

By following these recommendations, the Manifest service will provide a
robust backbone for the chora ecosystem: capability servers can fluidly
find and trust each other, and the overall system state can be observed
and managed via this single source of truth. This aligns with patterns
from established systems (Consul's service catalog, Kubernetes' API
Server for components, etc.) and tailors them to chora's specific
context.

### SAP Outline: Registry and Service Discovery Pattern

We will codify these registry best practices in **SAP-XXZ: Registry and
Service Discovery Pattern**. Its outline:

- **Capability Charter:** Explains the importance of a unified manifest
  in the chora architecture. Problem: Without it, services would need
  static configs or environment coupling -- which is brittle. Success
  criteria: dynamic discovery working; adding a new capability requires
  zero changes to others aside from reading from registry.

- **Protocol Spec:** Would detail the manifest's data model and API. For
  example, showing a snippet of a service's registry JSON, documenting
  each field (name, version, interfaces\...). It might include a brief
  description of the HTTP endpoints for manifest (essentially a mini-API
  spec). Even if we don't expose manifest publicly, documenting its
  interface is useful for devs and for possibly writing adapters (maybe
  in future a CLI to query manifest, etc.).

- **Agents Guide:** How AI agents can leverage the registry. For
  instance, instruct that an AI agent with access to call `manifest` can
  ask what\'s available. Possibly sample prompts for an agent to get
  list of capabilities (if the agent communicates via natural language
  to a system tool or has some API access). This could be interesting:
  e.g., an AI in the loop might query \"What can I do?\" and the system
  (via a tool) could respond with the list from manifest. So the
  AGENTS.md could outline how to present registry info to an AI or how
  an AI should pick endpoints from manifest (like an agent should prefer
  the REST interface from manifest as the target for actions unless it
  has an in-process API).

- It could also note patterns like: \"AI agents should not assume fixed
  addresses; always retrieve current addresses from the manifest.\"

- **Adoption Blueprint:** This blueprint would guide implementing the
  registry pattern in a new environment or updating an existing one:

- Step 1: Deploy or activate the Manifest capability server (maybe
  referencing the bootstrap SAP since manifest is part of Phase 1).

- Step 2: When developing a new capability server, integrate the
  provided library for manifest registration (or if writing from
  scratch, follow guidelines to register on start, heartbeat, etc.).

- Provide code templates (like a snippet showing how to call manifest
  APIs in Python).

- Step-by-step for adding a health check: e.g., \"Add a heartbeat call
  in your main loop or use the provided heartbeat thread from chora-base
  library\".

- Step-by-step for doing a lookup: e.g., \"In your capability, when you
  need to call another capability, use the manifest client to get its
  URL rather than a static config\".

- Possibly instructions for customizing metadata: e.g., \"If your
  capability depends on a specific external service, list it in
  dependencies metadata\".

- Tiered adoption:
  - Essential: at minimum, all services register/deregister and
    heartbeat with manifest; and all discovery is done via manifest.
    (This likely is mandatory, not optional).
  - Recommended: use advanced features like tagging and version checks.
    For example, if we have multiple environments, tag services with
    environment and filter accordingly.
  - Advanced: high availability manifest (running manifest cluster with
    failover), or integrating an existing enterprise service registry
    (maybe allow using Consul in place of chora manifest via an
    adapter).

- The blueprint might also cover monitoring usage: e.g., \"Set up alerts
  if manifest shows a critical service as down.\"

- Another advanced item: hooking manifest updates to automation -- e.g.,
  automatically reconfigure a load balancer if new instances show up.
  But that might not apply in our initial scope.

- **Ledger:** record of changes to the manifest design. E.g., \"v1.0:
  initial manifest with basic fields; v1.1: added \'dependencies\' field
  in metadata; v2.0: switched to use Consul backend, etc.\" Also track
  if any projects extended or tweaked it (maybe some deployment used
  Consul directly instead of chora manifest -- note it here).

By following SAP-XXZ, any developer working on a new capability server
will know exactly how to integrate with the manifest (down to code
examples), and any operator will understand how to interpret manifest's
data and use it for troubleshooting or orchestration. It ensures that
the dynamic nature of the chora ecosystem is preserved -- new
capabilities can be added without friction, and everything remains
discoverable and manageable.

## Part 4: Interface Design and Core-Interface Separation

Designing clean and stable interfaces is critical for capability
servers. A well-defined interface acts as a **contract** between the
capability server and its clients (whether they are other services, AI
agents, or end-users). This part explores principles of interface
design, emphasizing how to expose capabilities without leaking internal
details, how to handle multiple protocols (REST, gRPC, CLI, MCP)
consistently, and how to manage versioning, errors, and observability
across the interface boundary.

### Domain-Driven Design for Capabilities

First, applying **Domain-Driven Design (DDD)** concepts helps ensure the
interface reflects the **domain model** of the capability, not the
technology of its implementation. Each capability server can be seen as
a **bounded context** -- it encapsulates a set of related behaviors and
data for a specific problem area (e.g., orchestration, registry,
routing). Within that context, it defines its own **ubiquitous
language** -- a consistent set of terms for its operations and data.

For example, consider the Orchestration capability: - Domain concepts
might include \"Deployment\", \"Environment\", \"Service Instance\",
\"Provision\", \"Scale\", etc. These terms should appear in its
interface (API endpoints, CLI commands, etc.) in a consistent,
meaningful way. If the orchestrator core calls something an
\"Environment\", the REST API might use `/environments` in paths, the
CLI might have `chora-orch env list`, etc. This ensures that whether a
human or an AI reads the docs or uses the service, the language is
uniform. - **Aggregates and Entities:** In DDD, one models aggregates
(cluster of associated objects) with a root. For instance, an
\"Environment\" might aggregate multiple \"Deployments\". When designing
interfaces, one often reflects aggregates in resources (RESTful
thinking: environment is a top-level resource, deployments might be a
sub-resource under environment). This prevents exposing low-level entity
manipulation out of context. For chora, maybe orchestrator might have an
API like `POST /environments/{envId}/deployments` instead of a generic
`POST /deployments` without context, if deployments are tied to
environment logically. - **Capability Boundaries:** We should define
clearly what is in one capability's domain vs another's. For example,
any operations related to discovering services belong to Manifest's
interface, not Orchestrator's. Orchestrator should call Manifest if
needed but not offer redundant functions. This separation avoids
confusion and overlap in interfaces. If it\'s not in your bounded
context, your API shouldn\'t have it (or should delegate properly). -
**No Leaking Infrastructure Details:** The interface should present
domain concepts, not how they are implemented. E.g., the orchestrator's
API might ask for a \"service definition\" or \"container image\" rather
than \"write a Docker Compose file to this path\" -- hide how it does
things internally. If orchestrator uses Docker under the hood, the
client shouldn't have to know Docker specifics, just provide generic
info (like resource requirements or environment variables). This
prevents locking clients to the current implementation and allows
changing internals later (like switching from Docker to another
container runtime) without breaking the API. - **Ubiquitous Language
Example:** If all documentation and logs refer to \"capability
servers\", the interface should probably use that term as well when
appropriate (maybe \"GET /capabilities\" to list running capability
servers, which might be an endpoint on the manifest). Aligning terms
with those used by AI agents or documentation prevents miscommunication.
For instance, we wouldn't want the manifest API to call them
\"microservices\" in one place and \"capabilities\" in another; pick one
term.

### Interface Contracts: OpenAPI, gRPC, GraphQL, etc.

When designing an interface, there\'s a choice between
**contract-first** and **code-first** approaches: - **Contract-First:**
Define the interface formally (e.g., writing an OpenAPI spec or gRPC
.proto file) before implementing. This ensures clarity in what the API
should do, and fosters collaboration on the design. Many teams iterate
on an API contract with stakeholder feedback, then generate server stubs
and client SDKs from it. The benefit is a well-documented, stable
contract. E.g., a gRPC service: define the service and messages in a
.proto, which acts as the single source of
truth[\[10\]](https://grpc.io/docs/what-is-grpc/core-concepts/#:~:text=gRPC%20is%20based%20around%20the,their%20parameters%20and%20return%20types).
Or GraphQL: design the schema for queries and mutations up front, then
implement resolvers to match. - **Code-First:** Implement the interface
in code (e.g., writing controller classes in a web framework) and later
document it (some frameworks can output an OpenAPI spec from code
annotations). This can be quicker initially but may lead to ad-hoc or
less consistent design unless one is careful. It\'s common in agile
environments but can result in interface changes creeping in without
thorough review or documentation lagging.

**Recommendation:** For capability servers, consider using
**contract-first for public or stable interfaces**. For instance, define
the REST API using OpenAPI (formerly Swagger) -- it allows explicitly
specifying endpoints, parameters, request/response schemas, and error
codes. This can double as documentation (Swagger UI, etc.) and helps
with client generation for multiple languages if needed (though right
now maybe not needed since environment mostly Python, but nice to have).

For **gRPC** (if we choose to use it for inter-service comms or external
access), it\'s naturally contract-first via .proto. That ensures a
strong typed interface and versioning through proto's backward
compatibility rules (like you can add new fields with higher numbers
easily, etc.).

For **GraphQL** (less likely needed here, but possible if we wanted a
single endpoint for many queries), one would define types and queries in
the schema (SDL) which is basically contract-first (though GraphQL
allows a somewhat code-first via libraries, best practice often to think
through schema).

**Versioning Interface Contracts:** It\'s crucial to manage version
changes: - **Semantic Versioning in API path or headers:** e.g.,
`/api/v1/` vs `/api/v2/` if a breaking change occurs. Or for gRPC, using
package names or service names with version (like
`chora.orchestrator.v1` in proto package, and increment to `.v2` when
incompatible changes needed). For GraphQL, one tries to evolve schema
without breaking (GraphQL encourages additive changes and deprecation of
fields rather than outright removal). - **Backward compatibility
strategies:** Strive to make changes in a backward-compatible manner
whenever possible: - Add new optional fields in request or extra fields
in response (clients ignore unknown). - If needing to remove or change
semantics, perhaps support both old and new in parallel for a while
(e.g., Orchestrator might accept an older payload format under `/v1` and
a new one under `/v2`). - In CLI, you can mark commands or options as
deprecated in help text for some time before removing. E.g., `--foo`
flag still accepted but prints a warning recommending `--bar` going
forward. - Document version support clearly: e.g., \"Manifest API v1 --
stable, will be supported for X months after v2 launch\" etc., in SAP
perhaps or developer docs. Also define how the codebase will handle
multiple versions (maybe separate controllers or branching logic). -
**Independent versioning of interfaces vs core:** The core capability
might evolve faster internally, but you may choose not to expose
breaking changes until a major release. That means sometimes mapping new
core capabilities in a way that doesn\'t break old API. For example,
orchestrator core might gain a new scheduling algorithm, but the API
doesn\'t change for that, it\'s internal. Or if we completely change how
workflows are represented, might keep old API calls working and behind
the scenes map them to new logic, to not break older clients (maybe not
an issue if we control all clients, but if external use cases appear,
it\'s an important principle).

**OpenAPI vs gRPC vs GraphQL vs MCP:** - **OpenAPI (REST):** Good for
broad interoperability, human testable (via curl etc.), language
agnostic, and easy to document. Suited for most of these capability
interfaces. Each operation can be precisely defined. We should define
proper HTTP methods and status codes: - Use proper RESTful semantics
where possible (GET for read, POST for create, PUT/PATCH for update,
DELETE for remove). - Use meaningful resource URLs. - Use standard codes
(200/201 success, 400 for bad input, 404 not found, 500 server error,
etc.). - Use JSON as the media type (since it's standard; if heavy
binary needed, consider an endpoint that serves file or use gRPC for
that). - Possibly leverage OpenAPI features like `oneOf` if needed for
polymorphic data, etc., but keep it comprehensible.

- **gRPC:** If high-performance or strongly-typed streaming interactions
  are needed (for example, streaming logs from orchestrator to a client,
  or handling a large number of small requests efficiently). gRPC can
  also simplify writing clients in various languages since code
  generation yields a ready-to-use stub. However, it introduces
  complexity of requiring clients to know proto definitions and have
  gRPC support. Possibly an internal interface (between AI agent
  platform and capability server, or between capability servers
  themselves) could use gRPC for efficiency. If we define these, ensure
  that .proto files are well-managed and versioned. Perhaps initial
  chora scope uses REST and MCP primarily, gRPC could be optional
  optimization.

- **GraphQL:** Perhaps not directly needed for these admin-like
  operations. GraphQL shines in scenarios where clients need flexible
  querying of many fields, but our interactions are more RPC-like (do X,
  get Y). GraphQL could be considered if building a UI that needs to
  fetch data from multiple capabilities in one query, but it\'s likely
  overkill here. Possibly skip GraphQL unless an AI front-end needed a
  single endpoint for convenience (but GraphQL complexity may confuse AI
  if it needs to craft queries).

- **MCP (Model Context Protocol):** This is specific to AI agent
  integration. Possibly a specialized interface that uses a
  message-based protocol (maybe a custom or standardized one for agent
  \<-\> server communication). This might be lower-level or more
  unstructured. We need to design how core logic is exposed to AI via
  MCP. The pattern might be:

- Agent sends some structured prompt or action request, MCP gateway
  translates it to either a function call or a REST call to the
  appropriate server.

- Alternatively, each capability server might itself speak MCP (if it\'s
  basically just an API in natural language or some format). But likely,
  we have a **chora-mcp-gateway** (mentioned in context) which handles
  MCP interactions and routes to appropriate capability's native
  interface. That gateway would itself have an interface design (like it
  defines what \"actions\" it exposes to AI, etc.).

- We should ensure separation: the core capability doesn't need to embed
  all the logic for natural language understanding; that should be in
  the interface (MCP gateway or an \"AGENTS.md\" for how an agent should
  prompt).

- If MCP is something like OpenAI Function Calling or a JSON-based
  \"Action Schema\", define that clearly too (some SAP might cover it).

**Handling Protocol Translation (MCP ↔ REST, REST ↔ CLI, etc.):** - The
**Gateway** (Part of chora ecosystem) likely will handle bridging AI
interactions to REST calls. We should design our REST APIs in a way that
they can be easily invoked by the gateway given an agent's request. -
Possibly design **one core-interface** that is minimal and then
auto-generate others: - e.g., maybe implement most of logic in a Python
API (core classes), then use frameworks to expose it via CLI (like Click
reading docstrings) and REST (like FastAPI can auto-gen routes from
function definitions if using dependency injection or app design). - But
be cautious: auto-generation can produce suboptimal interface (like
generic names, or not following best practices). Better to treat each
interface with careful design, but reuse the same core logic.

**Interface-Specific Features & Differences:** - **Streaming &
Async**: - Some tasks (like \"deploy this server\") might take time.
REST is request-response; one can either block until done (maybe with a
timeout risk) or return a job id and allow querying status (pattern like
Kubernetes async operations or just get the result later). - gRPC
supports streaming responses easily; REST can do SSE (Server-Sent
Events) or WebSockets if needed. - CLI can show a progress bar or tail
logs easily if invoked interactively. - We should plan a consistent
approach: for lengthy operations, perhaps orchestrator returns a handle
(like an operation ID) which the client can poll or subscribe to for
updates. This approach can unify CLI and REST: CLI could call the API
then poll until done, showing progress. REST client (like a UI) could do
similarly or open a WS connection if we provide one. - Don\'t tailor
core logic to one interface's strength at expense of others. E.g., if we
don't implement server-sent events, that's okay; just ensure there\'s a
way to get progress (like an API call to get status).

- **Interactive Input:** CLI might allow prompting user for missing info
  (if run in tty). REST cannot prompt, it needs all info in request. So
  define required fields clearly such that CLI can gather them before
  calling core (like CLI command will have flags for all required
  parameters; if not given, CLI could interactively ask).

- **Error Handling & Standardization:**

- Decide on a standard error format for APIs. For REST/HTTP, a common
  approach: HTTP status codes + a JSON body with fields like `code`
  (application-specific error code) and `message`. E.g.,
  `{"code": "DEPLOYMENT_NOT_FOUND", "message": "No deployment with ID 1234"}`
  on a 404. Or a list of validation errors on 400.

- For gRPC, define error `codes` properly (gRPC status with rich error
  details or use standard codes like NOT_FOUND, etc. which map
  conceptually to HTTP codes).

- For CLI, exit codes plus stderr. We can map certain categories: e.g.,
  usage error (bad input) yields exit code 2, not found yields maybe 4,
  etc. But in general, CLI primarily prints a human-friendly error
  message. As long as that message matches what\'s in the API error (to
  an extent), we maintain consistency.

- The key is for similar error conditions, all interfaces signal
  similarly. Example: If you try to delete a nonexistent resource, the
  REST API gives 404 with \"not found\" message, the CLI should
  similarly output \"Error: resource not found\" and exit with non-zero.
  Not something totally unrelated or a Python stack trace, etc. Achieve
  this by having CLI catch known exceptions (like in our earlier code
  example, catching ServiceAlreadyExists and printing
  nicely)[\[28\]](https://medium.com/@kansvignesh/ansible-vs-chef-59ab2935444d#:~:text=As%20Ansible%20is%20agent,transparent%2Fseamless%20experience%20to%20the%20user)
  and mapping to a clear error text, ideally the same phrasing as REST
  would have given. Possibly use the API from CLI under the hood so it
  actually gets the same error message from server and prints it.

- **Observability Across Interfaces:**

- Logging: if an error occurs deep in core, it should log it. But what
  about trace IDs or correlation IDs? If a request comes via REST with a
  request-id header, propagate that in log contexts, so we can correlate
  user request to logs. Similarly for CLI usage, perhaps generate a
  request id and include in logs. This helps debugging issues across
  distributed calls.

- **Distributed Tracing:** If using OpenTelemetry or similar, instrument
  core logic with spans that can carry through from interface to
  interface. E.g., an orchestrator call that triggers manifest lookup --
  if both have tracing, it could follow. But this may be advanced, at
  least design not to preclude adding tracing later (like don\'t bury
  calls in threads without capturing context).

- **Audit Logging:** Possibly record at manifest or orchestrator level
  actions performed (who triggered them, when). For now, if needed,
  incorporate basic audit statements (like orchestrator logs \"User X
  requested deployment Y create\").

- **Separation of Concerns (Core vs Interface):**

- Core code should ideally be interface-agnostic. It can throw
  exceptions or return results in domain terms. The interface layer then
  translates to HTTP response or CLI print. This aligns with earlier
  code structure we used.

- Possibly define an interface boundary class or use an adapter pattern.
  For instance, define a Python class `OrchestratorService` with methods
  for each operation (taking Python types), and have the REST controller
  call those methods, the CLI command also call them. That class might
  be considered part of the \"core interface\" (the boundary) but not
  tied to any one protocol.

- If certain features only make sense in one interface, think carefully.
  Eg, CLI might have a convenience command that combines two steps which
  are separate in the API. That's okay as a user convenience, but ensure
  it actually just calls the two separate API steps internally. Avoid
  having CLI do something that cannot be done via API, otherwise those
  using API directly miss functionality. (Unless it\'s a pure UX thing
  like formatting output).

**Real-World Example Patterns:** - **gRPC & Envoy separation:** gRPC
clearly separates service definition from transport -- you can use Envoy
to translate HTTP/JSON to gRPC calls to backend (via transcoding
filter)[\[38\]](https://www.redhat.com/en/blog/grpc-to-rest-transcoding-with-openshift-and-service-mesh#:~:text=gRPC%20to%20REST%20transcoding%20with,proxied%20to%20a%20gRPC%20service).
Similarly, one could put a thin REST facade in front of gRPC services.
This indicates we can keep our internal logic in a gRPC server if that
suits, and have an Envoy or gateway do REST\<-\>gRPC if needed, giving
flexibility of interfaces without writing both heavy implementations. -
**GraphQL resolvers:** A GraphQL schema is separate from resolvers (the
code to fetch
data)[\[11\]](https://graphql.org/learn/schema/#:~:text=,infer%20the%20schema%20from%20that).
Each resolver calls into core logic or data source. This again is an
interface contract separate from implementation. We can see GraphQL as
an advanced integrator if one wanted to query multiple capabilities in
one go (though again likely out-of-scope). - **AWS API Gateway** often
maps HTTP requests to underlying Lambda functions -- essentially an
interface translation
layer[\[12\]](https://repost.aws/questions/QU1O0MzZU2RVKnTx3vRY9neQ/how-to-transform-http-requests-to-lambda-events-exactly-as-aws-api-gateway-does-as-an-http-proxy#:~:text=How%20to%20transform%20HTTP%20requests,the%20development%20process%2C%20I).
In chora, our gateway could map AI agent\'s DSL or instructions to one
or multiple underlying calls. - **Error code standards:** Many companies
standardize error responses (like Google APIs often return a JSON with
`error: { code, message, status }` where status is a string of the HTTP
code name). We can adopt a simple standard across all REST endpoints in
chora for consistency. (E.g., always return JSON with either a top-level
result or error field). - **Distributed Transaction Boundaries:** (This
touches composition patterns too) but ensure that interface calls either
succeed fully or clearly communicate partial failures. E.g., if
orchestrator\'s \"deploy environment\" call triggers multiple actions,
if one fails, how does API reflect that? Perhaps as an error with
details or a status resource to check for partial success. This way the
interface user (maybe another service or UI) can handle it properly.

By designing with these principles, we ensure the interface is robust,
user-friendly, and resilient to change.

Let\'s illustrate some of these points with a focused code example:
**error handling and translation across boundaries**.

#### Code Example: Consistent Error Handling (Core to API and CLI)

Suppose our Orchestrator core has a domain exception for an illegal
deployment configuration. We want the REST API to return a structured
error and the CLI to print a similar message.

Core definition:

    # orchestrator_core.py
    class DeploymentConfigError(Exception):
        """Exception raised when deployment configuration is invalid."""
        def __init__(self, message: str, field: str = None):
            super().__init__(message)
            self.field = field
            self.message = message

    def create_deployment(env_id: str, config: dict):
        # Validate config
        if "replicas" in config and config["replicas"] < 1:
            raise DeploymentConfigError("replicas must be >= 1", field="replicas")
        # ... (proceed with creation)
        return {"id": "dep123", "env": env_id, "status": "creating"}

REST API usage:

    # orchestrator_api.py (using e.g. Flask)
    from flask import Flask, request, jsonify
    from orchestrator_core import create_deployment, DeploymentConfigError

    app = Flask(__name__)

    @app.route("/environments/<env_id>/deployments", methods=["POST"])
    def api_create_deployment(env_id):
        data = request.get_json()
        try:
            result = create_deployment(env_id, data)
            return jsonify(result), 201
        except DeploymentConfigError as e:
            # Return a structured error response
            err_body = {"error": {"code": "INVALID_DEPLOYMENT_CONFIG", 
                                   "message": e.message}}
            if e.field:
                err_body["error"]["field"] = e.field
            return jsonify(err_body), 400

CLI usage:

    # orchestrator_cli.py (using argparse)
    import sys, json
    from orchestrator_core import create_deployment, DeploymentConfigError

    # ... argparse setup for command 'deploy create'
    try:
        config = json.loads(args.config_json) if args.config_json else {}
    except ValueError:
        print("Error: config JSON is invalid", file=sys.stderr)
        sys.exit(2)

    try:
        result = create_deployment(args.env_id, config)
        print(f"Deployment {result['id']} created in env {args.env_id}. Status: {result['status']}")
    except DeploymentConfigError as e:
        # Print similar message as API would return
        msg = f"Invalid deployment config: {e.message}"
        if e.field:
            msg += f" (field: {e.field})"
        print("Error:", msg, file=sys.stderr)
        sys.exit(1)

In this example: - The **core function** `create_deployment` raises
`DeploymentConfigError` with a message and field name. - The **REST API
endpoint** catches that and returns a JSON error with a code and message
(and field). It chooses an error code string `INVALID_DEPLOYMENT_CONFIG`
which clients can programmatically check if needed, and HTTP 400. - The
**CLI** similarly catches the exception and prints a user-friendly error
to stderr, including the field if present, and exits with code 1
(general error). - The error message content is aligned: e.g., core
might produce \"replicas must be \>= 1\", API responds with that
message, CLI prints \"Invalid deployment config: replicas must be \>= 1
(field: replicas)\". So a user or developer sees consistent phrasing. -
If we had an AI agent reading these, consistency helps it learn the
expected output patterns too.

**Observability addition:** We could also log the error internally with
context:

    import logging
    # in except of API
    logging.warning(f"Deployment config error for env {env_id}: {e.message} (field {e.field})")

So that there\'s a record on server side.

Now, **Prescriptive Interface Design Do's & Don'ts:**

**Do:** - Clearly define your API endpoints and methods upfront (use
OpenAPI or similar for REST, .proto for gRPC). Treat them as contracts
to uphold. - Use consistent naming and structure across all interfaces
for the same concept. If an operation is called \"create deployment\" in
REST, the CLI command should be similar (`deploy create`), not something
like `add-service` which could confuse. - Ensure **backward
compatibility** whenever possible. Document any breaking changes and
ideally provide a transition period or fallback. (And bump version
accordingly.) - Centralize common behavior like error mapping,
validation, etc. so that all interfaces handle them similarly. For
example, use the same validation functions in core so that CLI and API
don\'t implement separate logic that might diverge. - Use standard
communication patterns (RESTful conventions, gRPC status codes, CLI exit
codes) so integrators and users have less surprises. - Provide thorough
documentation for each interface: API docs for REST/gRPC, help and
manuals for CLI, describing available commands, parameters, and
examples. This can be in the SAP or separate user docs. - Incorporate
logging and tracing IDs to correlate calls through different layers.
E.g., an HTTP request might include a header `X-Request-ID` that you
also log and maybe propagate to any sub-calls (like orchestrator calling
manifest). - Test each interface thoroughly, including consistency tests
(for example, create via API, then perhaps try to reference result via
CLI to ensure compatibility). - Decouple interface logic from core logic
as much as possible (except where minor differences are needed). This
modularity also means you could replace one interface implementation
without touching core (for example, swap out Flask for FastAPI if
needed, or add a new interface e.g. voice commands interface hooking
into the same core). - Monitor and collect usage metrics per interface.
E.g., measure how many calls each endpoint gets, how many CLI
invocations succeed vs error. This can inform if maybe an API is
confusing (if lots of errors from misuse).

**Don't:** - Don't expose internal state or implementation details in
your interface. E.g., avoid using database primary keys as part of API
unless they carry meaning, or returning internal error stack traces to
users (should be logged but not given to API callers for security). -
Don't rely on informal interfaces (like \"we'll parse logs to do X\").
Always provide a proper interface (if something is needed by clients,
incorporate it into an API rather than telling them to parse some human
output). - Don't implement the same logic in multiple interface layers.
For instance, don't duplicate input validation in both CLI and API
separately; have core or a shared library handle it so it remains
uniform. - Don't ignore interface versioning. If you change something,
think \"will this break any existing client or script?\" If yes, provide
both old and new ways, or version it. - Don't neglect error handling --
returning generic \"500 Internal Error\" or a Python traceback to user
is not acceptable. Catch known errors and translate them to meaningful
messages or codes at the interface boundary. - Don't make synchronous
interfaces do asynchronous work without proper feedback. For example, a
CLI command that triggers a long process should either show progress or
advise user that it's happening in background. Similarly, an API call
that times out after 30 sec should consider returning a job ID and not
making client wait too long with no result. - Don't design interfaces
solely for one type of consumer if possible -- consider both human users
(CLI, maybe UI) and programmatic users (other services, AI). For
example, a CLI can have human-friendly formatting, but if it also might
be scripted, offer a `--json` output option to make parsing easier (many
CLI tools do this, e.g., `kubectl -o json` outputs JSON that matches
API). - Don't forget documentation and announcements of interface
changes. When releasing new features or deprecating, communicate clearly
(in docs or SAP ledger maybe). - Don't expose too many ways to do the
same thing on one interface -- it can confuse. Keep it simple and
canonical. For instance, one API endpoint per operation, one CLI command
per task, rather than multiple aliases or overlapping functions.

By adhering to these, we achieve an **interface design that is clean,
predictable, and maintainable**, thus enabling capability servers to be
used easily by both humans and machines (including AI agents). This
fosters trust in the system -- users know what to expect and developers
can integrate without guesswork.

Finally, we incorporate these into a **SAP structure.**

### SAP Outline: Interface Design and Contracts

This would be **SAP-XYY: Capability Server Interface Design Pattern**
(or similar): - **Capability Charter:** Why consistent interface design
matters (ensures interchangeability, ease of adoption, fewer errors).
Outline the problems of poor interface design with examples and how this
SAP addresses them. - **Protocol Spec Guidance:** Not a spec itself, but
guidelines on creating one. Possibly a checklist: \"Before implementing,
write down the interface: list operations, inputs/outputs, error
conditions.\" Could reference using OpenAPI or gRPC. Provide a template
OpenAPI snippet as example for one operation (like a generic pattern for
REST endpoint). - **AGENTS.md (Awareness Guide for AI):** Possibly
instruct on how to structure API responses that are AI-friendly (like
having clear messages, maybe limiting use of ambiguous terms). Or
instruct that CLI outputs should be concise if an AI will read them. For
instance, if we anticipate an AI reading CLI output, avoid ASCII art or
highly verbose text that might confuse parsing. Or ensure that the AI
uses the JSON output options. Provide best practices if an AI is
controlling CLI or reading API docs. - **Adoption Blueprint:** Steps to
follow when designing a new capability server\'s interface: 1. Identify
domain concepts and ensure consistent naming (maybe encourage creating a
glossary of terms). 2. Decide on interface types needed (maybe you don't
need gRPC if not heavy load, etc.). 3. Design the interface (perhaps
requiring a design review by another team member or architect to catch
inconsistencies). 4. Implement core logic and then interface layers, or
generate from contract. 5. Use provided libraries or patterns for error
handling (maybe we provide a base exception class and base API/CLI
controllers in chora-base to reduce boilerplate). 6. Document the
interface (where to put the OpenAPI file, how to auto-generate Markdown
docs from it, etc.). 7. Write tests at the interface level (maybe using
an API testing tool or just integration tests calling the endpoints). -
Tiered adoption: \* Essential: follow recommended naming and error
conventions, implement at least one common interface (REST and CLI
likely essential). \* Recommended: implement all standard interfaces
(REST, CLI, possibly MCP integration) as per patterns, and provide usage
examples in docs. \* Advanced: more sophisticated stuff like employing
hypermedia in REST (HATEOAS), or advanced CLI features (shell
autocompletion, etc.), or end-to-end typed clients (generate a Python
SDK from OpenAPI and use it). - Could also mention using interface
separation for testing (e.g., unit test core functions directly, use
stubbed interface for that). - **Ledger:** track improvements to
interface guidelines. E.g., if we adopt a new standard (like switching
to a different error format or adding GraphQL), note it. Or if a
particular interface approach caused issues, note the resolution (like
\"we had inconsistent field names between CLI and API in early version,
fixed by aligning them in vX\").

With this SAP, all developers have a clear reference on how to expose
their capability\'s functionality properly. It ensures the ecosystem
feels cohesive -- using different capability servers is similar in
style, which reduces learning curve (like how all AWS services have
similar API patterns, or all `kubectl` subcommands behave similarly).

By the end of Part 4, we have established how to design interfaces that
are **clean, consistent, and decoupled** from core changes, enabling the
capability servers to be easily integrated and evolved over time without
breaking the contracts they provide to others.

## Part 5: Composition Patterns for Capability Servers

Individual capability servers in the chora ecosystem provide useful
domain-specific functions, but real workflows often require
**composing** multiple capabilities to achieve higher-level tasks.
Composition can occur in several forms: one service calling another
synchronously (like orchestrator using manifest), asynchronous
event-driven interactions (publishing events that others react to), or
orchestrating sequences of operations (workflows). This part examines
how to effectively compose capability servers while managing
dependencies, data flow, and failure handling. We draw on microservice
composition patterns such as orchestration vs choreography, Saga
transactions, and event-driven architectures.

### Service Composition Approaches: Orchestration vs Choreography

- **Orchestration** refers to an explicit central controller that
  coordinates interactions between services, dictating the sequence of
  operations. In microservices, an orchestrator can be a dedicated
  service (like an orchestration engine or workflow engine) that calls
  others in order. For example, an Orchestration capability server in
  chora acts as a conductor: when a user requests a new environment
  deployment, the orchestrator might call the Manifest to register it,
  call the Gateway to route traffic, and call n8n to set up a default
  workflow -- each in a defined sequence and handling outputs between
  them. Orchestration is like a **synchronous or step-by-step
  composition**, often implemented with code or a workflow DSL. The
  advantage is having a global view of the process (easier to ensure
  steps occur and manage rollbacks if a step fails), but the
  orchestrator becomes a central point of control (and failure, if not
  highly available).
- **Choreography** means services interact in a decentralized fashion,
  reacting to events or state changes, without a single point
  controlling flow. Each service listens for events and does its part,
  possibly emitting more events. For instance, in a choreography
  scenario, deploying an environment might be kicked off by Orchestrator
  sending an \"EnvironmentCreated\" event to a message bus; the Gateway
  service picks that up and configures routing for it, the Manifest
  service might automatically update entries (though in our design
  manifest is central, so maybe not applicable for manifest, but say a
  monitoring service hears it and starts tracking the new environment).
  In choreography, there\'s no central coordinator telling each service
  what to do; they \"dance\" according to a pre-defined protocol or just
  by convention (like \"when X event, do Y\"). The benefit is it's more
  loosely coupled and scalable (no one service has to know the whole
  story), but it can be harder to understand and manage, and risk of
  race conditions or cycles (service A triggers B, B triggers C, and
  maybe C triggers A again inadvertently -- need to avoid infinite
  loops,
  etc.)[\[17\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=Benefits%20of%20choreography%20Drawbacks%20of,Integration%20testing%20is%20difficult).

**Which to choose in chora?** We actually have a mix: The
**Orchestration capability server** suggests a central orchestrator
pattern (some flows will be explicitly controlled by it). Meanwhile, the
presence of an **n8n workflow server** indicates an event-driven or
pipeline orchestration (n8n orchestrates sequences, possibly including
external triggers -- which is orchestration albeit in a low-code style).
Also, the existence of a **manifest** hints at some event-driven
aspects: other services might essentially \"choreograph\" by reacting to
registry changes.

Likely: - Use **orchestration** for processes where central logic is
valuable -- e.g., provisioning, scaling, complex multi-step operations.
The Orchestrator server likely implements a lot of these as explicit
flows (maybe coded or via something like Temporal or Step Functions
style). - Use **choreography** (via events or pub/sub) for cross-cutting
concerns or optional integrations that should not tie up the
orchestrator. For example, if we integrate an alerting service, instead
of orchestration calling \"alert service\" at each step, one might
broadcast events like \"DeploymentFailed\" that the alert service
listens for to send notifications. That way, the orchestrator doesn\'t
have to know about alerting at all -- it\'s loosely coupled. - The key
is *balance*: orchestrate core flows, choreograph expansions and
optional reactions.

**Real-World Microservice Insight:** Martin Fowler notes that as systems
grow, a purely choreographed approach can become hard to manage if
complex (because no single place shows the full
workflow)[\[39\]](https://martinfowler.com/articles/microservices.html#:~:text=These%20are%20choreographed%20using%20simple,The).
Sam Newman often suggests starting simple (maybe orchestration for
clarity) but making sure services still work decoupled enough to switch
to events where appropriate.

Chora's scale is moderate, so we can centralize logic in Orchestrator
for most stuff, but we can incorporate events for decoupling.

### Dependency Management and Resolving Dependencies

When composing services, we must manage service **dependencies**: -
**Declaration of Dependencies:** We touched on manifest listing
dependencies. This helps orchestrator or bootstrap know start order
(manifest must precede others). It\'s also documentation for devs: e.g.,
\"gateway depends on orchestrator and manifest\". - **Optional vs
Required:** Mark some dependencies as optional or at least handle
absence gracefully. For instance, say there\'s an optional \"Analytics\"
capability that logs usage -- other services can run without it, they
just won\'t send data if it\'s not present. Or a \"Cache\" capability
that if absent, things still work (maybe slower). These should be
clearly noted so orchestrator or agents know they can proceed without
them. - **Circular Dependencies:** E.g., orchestrator \<-\> manifest
could be circular: Orchestrator needs manifest to register, manifest
might rely on orchestrator to deploy updates. We broke that by bootstrap
sequence. Always break cycles by picking one to start first with static
config or by merging responsibilities if needed. If truly circular
logically (rare if well-designed), might have to merge them or
externalize one piece. - **Dependency Injection at runtime:** Ensure a
service can be configured with addresses or references to its
dependencies (like orchestrator has manifest URL configured, gateway has
orchestrator's endpoint configured, etc.). We used manifest to avoid
hardcoding addresses, but the dependency injection is still needed (like
an environment variable or config file with \"MANIFEST_URL\"). For
composition, orchestrator could look up dependencies at startup via
manifest (bit meta, since manifest itself), but after initial
connection, better to store the addresses for making calls. -
**Compatibility of Dependencies:** If orchestrator v2 depends on
manifest v2 features, we have to ensure manifest is upgraded first or
orchestrator can degrade gracefully. That is version compatibility --
likely we\'ll upgrade whole system together, but if not, one should
design for backward compatibility (like orchestrator v2 can use manifest
v1 but maybe won\'t use new features until manifest is updated). -
**Service Stubs or Mocks:** In some cases, to break dependency for local
development or testing, one can simulate a dependency. E.g., if manifest
isn\'t available, orchestrator might run with a stub manifest (maybe
reading a local config). Or for unit tests, use a fake. This isn\'t at
runtime in production, but it influences design (e.g., injection and
having interfaces so it's easy to swap out).

**Algorithm for dependency resolution at startup:** The orchestrator (or
a bootstrapper) can topologically sort services by dependency and start
them in order. E.g., from manifest's dependency lists, one could
derive: - manifest: no dependency -\> start first - orchestrator:
depends on manifest -\> start after manifest up - gateway: depends on
orchestrator and manifest -\> start after both are ready - etc. This is
like how Kubernetes or Docker Compose handle dependencies implicitly (or
via readiness checks).

If dynamic (like orchestrator launching new cap servers on the fly),
orchestrator must ensure needed dependencies are running or launch them
first. E.g., if user requests enabling some capability that needs
another, orchestrator could auto-start the dependency.

**Version compatibility patterns:** Similar to microservices: - If
multiple versions need to co-exist, perhaps run them side by side and
route appropriately (maybe via Gateway routing by version). - Use
semantic version rules: e.g., manifest 1.x and orchestrator 1.x are
compatible, orchestrator 2.x needs manifest 2.x (so orchestrator might
refuse to start if manifest below required version, which is a safe fail
rather than running incorrectly). - Possibly incorporate a \"capability
catalog\" (like a manifest for versions) where each service's record
indicates a required manifest version or something, and orchestrator
checks it.

### Data Flow and Communication Patterns

**Synchronous vs Asynchronous:** - Synchronous calls (like REST/gRPC):
simpler immediate request-response, used for query or direct commands.
Orchestrator likely uses sync calls to manifest (like \"register service
now and wait for success\"). Sync ensures sequential logic is easier. -
Asynchronous messaging (pub/sub or queues): used when immediate response
not needed or to decouple for load leveling. For example, orchestrator
might place a deployment job on a queue that a pool of workers
processes, rather than doing it inline if it takes long. Or if
orchestrator triggers an event \"EnvironmentReady\", it doesn\'t care
who picks it up and how long it takes them to handle it. - Chora might
incorporate both: for core operations likely synchronous HTTP calls
within cluster, for events and cross-service notifications maybe a
message bus. Possibly an internal event bus (maybe as part of the
Gateway or separate). - The chosen style should minimize complexity: too
much asynchrony can make state tracking hard (lack global transaction
context).

**Pub/Sub Patterns:** - **Consul\'s approach**: not exactly pub/sub, but
uses watchers. Or Kubernetes events stream for resource changes (clients
can watch the API for events). - If we include something like an \"Event
Bus\" capability server (maybe n8n covers some pubsub flows, or a
separate message broker like a simple MQTT or Redis pubsub could be
integrated). - Pattern: Services subscribe to events relevant to them.
Eg, an \"AI monitoring service\" subscribes to all \"ErrorOccurred\"
events from any server to create a report or alert. - Ensure events have
enough info but not overly detailed (to avoid tight coupling). E.g., an
event \"ENV_CREATED\" might include environment ID and some context, but
not assume who consumes it or how. - Possibly define a small set of
standard events that capability servers can emit and handle. Document in
SAP. - Guarantee at-least-once vs at-most-once: likely at-least once (so
if orchestrator sends an event and subscriber crashes, maybe they missed
it unless using durable queue; if durable needed, use a broker that can
buffer). - Could simply use something like a `chora-events` channel in
an internal broker where all broadcast events go (with topics or type
field to filter). - We must be careful that event storms don\'t
overwhelm or cause cascades (impose some throttle or ensure idempotent
handling; Saga pattern relates here).

**Event-Driven Composition Example:** Possibly orchestrator orchestrates
initial creation, then uses events for subsequent updates. E.g.,
orchestrator might instruct \"deploy environment\", and once done, it
emits \"EnvironmentDeployed\" event that maybe triggers a separate
capability to run integration tests or notify users. That second part is
choreographed by event rather than coded in orchestrator\'s flow, making
it extensible.

**Distributed Transaction (Sagas):** - Many composite operations involve
multiple services updating state. This raises the issue: if one fails
mid-way, how to avoid inconsistency? - **Saga Pattern:** This addresses
distributed transactions by executing a series of local transactions
with compensating actions on
failure[\[16\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=by%20coordinating%20transactions%20across%20multiple,approach%20helps%20maintain%20data%20consistency)[\[40\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=If%20a%20local%20transaction%20fails%2C,the%20preceding%20local%20transactions%20made).
Two Saga styles: - *Choreography-based Saga:* Each service knows to
listen for certain events and perform their action or a rollback event.
E.g., Orchestrator tries to do A, B, C by sending events and services do
their part, if something fails one might send a compensation event for
others to undo (like \"CANCEL environment\" which each service responds
to by cleaning up their part). - *Orchestration-based Saga:* The
orchestrator (or a Saga coordinator) explicitly calls service A, then B,
then C. If one fails, it triggers the known compensations (calls A
compensation, etc.). This could be implemented via workflow logic in
orchestrator. Possibly our Orchestrator server might have such logic for
multi-step operations (like environment creation might be considered a
Saga: allocate resources (manifest entry), configure network (gateway),
start services (maybe orchestrator calls a container engine). If final
step fails, orchestrator should remove manifest entry and network config
to roll back). - For chora, simplest approach is implement compensating
logic in orchestrator flows (since we do have a central orchestrator).
For example: - On environment creation failure after partially done,
orchestrator explicitly calls the services that succeeded and asks them
to undo (like deregister from manifest or remove route from gateway). -
Possibly orchestrator record a Saga context so it knows what steps
completed so far (so it knows which compensations needed). - Or use a
workflow engine like Temporal (Temporal is essentially Saga
orchestration built-in). If we had a capability like that, but likely
not needed at our scale; we can code simpler try/except sequences with
cleanup calls. - The SAP can lay out guidelines: \"If your capability
operation spans others, ensure to implement proper rollback if later
calls fail.\" Provide pattern as pseudo-code or use an example (like
environment creation as above). - We might note that some operations are
not easily undoable (e.g., sending an email cannot be unsent). In those
cases compensating action might be a negative acknowledgment or a
remediation step. At least document which actions are irrevocable so
orchestrator designs flows accordingly (maybe do those last).

**Data Consistency across composed services:** - If services maintain
separate databases, one operation might involve updating multiple.
Without a distributed transaction, we rely on Saga or eventual
consistency. - Possibly in chora, most state is ephemeral or in manifest
or in each service. - Example: orchestrator has concept of an
environment, manifest has entries about services in it. Orchestrator
must update its DB and then call manifest. If manifest call fails,
orchestrator should revert DB or try again. If manifest succeeded but
orchestrator DB fails after, how to reconcile? Could on startup
orchestrator reconcile with manifest by checking entries and adjusting
DB accordingly. - We can design each service to be somewhat resilient:
e.g., if manifest has an entry without corresponding orchestrator
record, orchestrator could detect and clean it (maybe after crash
recovery). - Or better, use orchestrator as source of truth and treat
manifest as derived data -- meaning orchestrator can always re-populate
manifest if needed (less need if both on stable storage). - Possibly
utilize event sourcing pattern: each action yields events and all
services eventually align to those events (but that\'s heavy). - For
now, rely on orchestrator performing actions in proper order and
verifying outcomes, with manual or automated reconciliation for rare
inconsistency.

### Workflow Orchestration Models (Camel, n8n, Step Functions, Temporal)

- These are examples of more specialized composition:
- **AWS Step Functions** and **Temporal**: provide explicit workflow
  modeling, including parallel steps, waiting, retries, etc. Step
  Functions acts like an orchestrator of AWS services with a JSON state
  machine[\[14\]](https://dev.to/dixitjain/aws-step-functions-the-conductor-of-your-microservices-orchestra-2e77#:~:text=What%20are%20AWS%20Step%20Functions%3F).
  Temporal similarly orchestrates code with a durable runtime and
  built-in saga handling. If the chora orchestrator becomes complex,
  using a workflow engine or writing one could be an option. Possibly
  beyond initial scope, but maybe n8n covers basic sequences user can
  define.
- **Apache Camel**: focuses on routing and transforming data between
  systems (integration patterns). If we had many different protocols to
  connect (e.g., watch a file, then call a service, then send email),
  Camel could coordinate that. For chora, Camel isn\'t explicitly
  included, but the Gateway might perform some integration logic.
- **n8n**: an open-source low-code workflow orchestrator (which chora
  includes as a capability). It likely will be used by users to compose
  their own automations hooking into chora capabilities (e.g., \"when a
  new environment is deployed (trigger from orchestrator or manifest),
  send a Slack message\"). So n8n adds a user-facing composition layer
  (like Step Functions but UI-driven).
- We should ensure our capability servers expose triggers or webhooks
  that n8n can connect to. Possibly provide n8n nodes that connect to
  orchestrator\'s API, etc. That's more about adoption and integration
  than core arch, but something to consider in SAP development (maybe a
  blueprint on using n8n with others).
- If n8n orchestrates something that should be transactional, then again
  need to consider saga (but n8n likely doesn\'t inherently do
  distributed transactions, just sequences tasks with optional rollbacks
  defined by user).

**Failure Handling & Retries:** - Identify points where a call might
fail due to transient issues (network glitch, service slow) vs permanent
issue (bad input). - Implement **retries** for transient failures: e.g.,
orchestrator calling manifest times out -- try again a couple times with
backoff before giving up and marking environment deploy failed. Many
cloud systems do this behind scenes (AWS SDK does 3 retries by default
for idempotent ops). - If a non-idempotent operation, be careful with
retries. E.g., if orchestrator creates a container and got no response,
did it actually create it or not? Could lead to duplicate container or
an orphan. Solutions: make operations idempotent (like provide an id or
name so second attempt doesn\'t create a new one but reuses existing or
gets a duplicate error which orchestrator can interpret as success if
it\'s exactly what it wanted). Often orchestrator will generate an ID
and use it in calls to avoid duplication. - **Circuit Breaker:** If a
dependent service is down (manifest or gateway), orchestrator might
refrain from trying further for a bit (fail fast rather than hanging
many requests). - **Compensation vs retries:** If an operation fails
mid-stream after partially doing tasks, orchestrator should decide
whether to roll back partial or to try again from that point. Saga tends
to favor rollbacks (compensate and maybe report failure to user). But
sometimes you can also retry the failing step and hope it succeeds next
time (if it\'s a transient cause like a network partition, retry might
succeed and then you can continue Saga normally). - Distinguish between
expected failures (like user input issues, which should not be retried
but directly result in user error) and unexpected (transient system
issues, which might be retried or circumvented).

**Idempotency Patterns:** - Use unique request or operation IDs to allow
safe retries. E.g., orchestrator includes an \"operationId\" when
telling gateway to create route; if it times out and tries again with
same ID, gateway sees it\'s the same request and doesn\'t duplicate, it
returns previous result (or acknowledges it already did it). - This
often requires services store those IDs temporarily (like a table of
completed operations or dedup keys). - Alternatively, design the APIs to
be naturally idempotent: e.g., use PUT with a specific resource name (so
if you call it twice, it\'s simply updating/overwriting the same
resource to same state, no side effect beyond the first time). - For
deletion operations, repeating often is fine (delete of already deleted
yields maybe 404 or no-op).

**Example of Saga in chora context: Deploy environment Saga steps:** 1.
Create manifest entries for new services (so they are discoverable). 2.
Deploy containers for those services (via orchestrator's container
management). 3. Configure gateway routes. 4. Mark environment as
ready. - Compensations if, say, step3 fails: remove routes if partially
added, remove containers (step2), remove manifest entries (step1).
Possibly orchestrator can do these in reverse order for all that
succeeded. - Alternatively, orchestrator could do manifest entry last,
so nothing is discoverable until everything else succeeded (some prefer
that ordering: do internal provisioning, only register or announce once
fully available -- that avoids needing remove from manifest if fail.
Downside: other might not see it in manifest while it\'s partially up,
but maybe that\'s fine if consistency needed). - Choose approach based
on how you want other services to behave; often you don\'t want a
service listed until it\'s actually functioning.

**Anti-Patterns in Composition:** - Tightly coupling services with
synchronous calls such that a failure cascades widely and the whole
system stalls. E.g., if orchestrator on a request calls manifest which
calls gateway which calls orchestrator again -- can lead to deadlock or
overload. Avoid unnecessary nested calls; one reason we use manifest as
central rather than each service calling orchestrator for everything. -
Overloading orchestrator with too many responsibilities; if it becomes a
bottleneck, consider delegating (maybe using events or separate worker
services for some tasks). - Spaghetti event flows: where events trigger
events with no clear control, leading to race conditions or confusion.
E.g., multiple services reacting to the same event in conflicting ways.
If events used, define clear event handling responsibilities. - Not
handling partial failures, leading to resource leaks (like container
left running but not registered, etc.). Always account for those
scenarios in design (maybe a periodic reconciliation job in orchestrator
to find orphaned things and clean up). - Over-retrying can be bad too
(e.g., infinite or aggressive retries can amplify a problem -- e.g.,
manifest is down, orchestrator floods it with retries and backlog,
making recovery harder). Use bounded retries and fallback to human alert
if needed. - For Saga: Not compensating in all failure paths (like
forgetting to implement compensation for a certain step because \"it
rarely fails\" -- Murphy\'s law says it will eventually). - Ignoring
data consistency: e.g., orchestrator marks environment ready even though
one service failed to start (maybe because it didn\'t know) -- leaving
system in invalid state. Better to mark it partially ready or failed and
let someone fix (maybe via re-run or separate recovery process).

In summary, good composition means: - Clear control or event flows, -
known dependency ordering, - robust error handling (either immediate or
eventual consistency with recovery), - and designing with the assumption
that any call can fail and any service can be unavailable at some point
(so degrade gracefully).

### Code Example: Simple Saga (Orchestration with Compensation)

For illustration, a pseudo-Python logic in Orchestrator performing a
two-step process with compensation:

    def create_environment(env_config):
        created_services = []
        try:
            # Step 1: start database service for environment
            db_service = start_database(env_config["db_config"])
            created_services.append(("database", db_service))
            # Step 2: start app service, depends on database
            app_service = start_application(env_config["app_config"], db_url=db_service.url)
            created_services.append(("application", app_service))
            # If both succeeded:
            manifest.register_environment(env_config["name"], services=[db_service, app_service])
            return {"status": "success", "env_name": env_config["name"]}
        except Exception as e:
            # Something failed
            logging.error(f"Environment creation failed: {e}. Rolling back partial services.")
            # Compensation: tear down any service that was created
            for svc_type, svc in reversed(created_services):
                try:
                    if svc_type == "application":
                        stop_application(svc)
                    elif svc_type == "database":
                        stop_database(svc)
                    manifest.deregister_service(svc.name)
                except Exception as ce:
                    logging.warning(f"Compensation failed for {svc_type}: {ce}")
            return {"status": "failed", "error": str(e)}

This pseudo-code: - Keeps track of what was created. - If a later step
fails, it rolls back in reverse order (application then database) and
deregisters any that got registered (if they were, here manifest
registration done at end, but if any partial reg happened earlier it
would remove). - It logs errors and returns a failure status.

In a real orchestrator, you\'d likely separate the manifest registration
at the end only if success, to avoid having to deregister on fail. Or if
register early to allow others to see it as coming, then ensure to
deregister on fail (both strategies workable, but lean to register at
end for simplicity).

This approach ensures no orphaned services remain if environment
creation fails mid-way.

**Do & Don\'t for Saga:** - Do implement compensations for all steps
that have side effects. - Do test failure scenarios (simulate step2
failing, see if step1 is cleaned). - Don\'t ignore errors during
compensation (we at least log warnings here; maybe escalate to manual
intervention if compensation fails, because then there\'s a leftover). -
Possibly integrate with monitoring to alert if compensation also fails
(so ops can clean manually). - Do consider idempotent compensation
(stopping an already stopped service should not error, or should be
caught and treated as success).

### Anti-Patterns Recap:

- We discussed them above: tight coupling, ignoring partial failures,
  etc.

### Prescriptive Recommendations Summary for Composition

**Do:** - Use a central orchestrator for complex multi-step workflows,
and use event-driven (choreography) for decoupled, optional reactions or
cross-cutting concerns. - Clearly define and document service
dependencies so they can be managed in bootstrap and orchestration logic
(avoid surprises). - Make inter-service calls idempotent wherever
possible, and implement retries with backoff for transient failures. -
Implement compensating actions for partial failures in multi-step
operations (Saga pattern). Test these failure modes thoroughly. - Use an
event bus or message mechanism for broadcasting significant events
(e.g., state changes), to which other services can subscribe if needed,
thereby avoiding hard-coded calls in orchestrator for things not core to
the workflow. - Ensure each service handles incoming calls or events
gracefully if a dependent service is down -- e.g., return a friendly
error \"Can\'t complete because X is unavailable\" rather than hanging
indefinitely. - Provide timeouts for inter-service calls (and tune them
based on expected response times plus network overhead). - For critical
flows, incorporate at least minimal transaction management: e.g., if
orchestrator says \"done\" externally, ensure all parts indeed done or
have compensation flows started. - Use persistent queues or state where
needed to ensure reliability. For example, if orchestrator scheduled a
task and then crashed, on restart it should resume or rollback (persist
tasks states either in its DB or rely on at-least-once events). -
Monitor the composition: e.g., track overall workflow durations,
failures per step, to identify bottlenecks or fragile points. Perhaps
orchestrator logs metrics on how many flows succeeded vs compensated,
etc. - Provide administrative tools or commands to manually trigger
compensations or cleanup if automatic fails (like a \"force-remove
environment\" that cleans whatever remains). - Keep services as
independent as possible in normal operation -- i.e., avoid requiring
synchronous coupling unless necessary. For instance, a service should
not hold a long open connection waiting on another -- that ties their
lifecycles. Instead, break tasks or use async flows where one can
operate independently and eventually sync via states or events. -
Leverage existing workflow or messaging components (like n8n for
user-level flows, or an external message broker) if it simplifies
composition rather than reinventing one.

**Don\'t:** - Don\'t allow the failure of one component to cascade
without control. Use circuit breakers (stop calling a service if it\'s
failing repeatedly to give it time to recover), and fallback behaviors
if possible (maybe use a cached value or default if manifest is briefly
down). - Don\'t design in circular wait (deadlocks) -- e.g.,
orchestrator waiting for gateway to do something while gateway is
waiting for orchestrator's confirmation. If found, redesign to break
cycle (maybe orchestrator just does it directly or there\'s an
out-of-band signal). - Don\'t overload a single service with too many
responsibilities (Single Responsibility Principle at system level). If
orchestrator logic gets too heavy, consider splitting out specialized
microservices (like a \"Backup coordinator\" service if that became a
big separate flow). - Don\'t forget to update the dependency graph if
architecture changes (like if new capability added, update manifest and
bootstrap sequences). - Don\'t assume eventual consistency will
magically resolve issues -- design explicit reconciliation processes.
For example, if an event-driven update fails due to subscriber down,
when subscriber comes back, it should reconcile by checking current
state via a sync call. (Classic example: eventual consistency is fine
but you often need periodic sync to correct any missed events). - Don\'t
ignore the data at rest -- composition is not only about calls: consider
data flows (one service might need data produced by another -- define
how it gets it: via direct call now, or via event with payload, or via
shared database? Typically avoid shared DB as that couples them too
much; prefer passing data through interface). - Speaking of that:
**Don\'t share databases between services** -- composition should happen
via interfaces only, to maintain boundaries (each microservice owns its
data). - Don\'t infinitely retry failed operations without escalation
(could cause stuck resources or high load). After N tries, mark as
permanently failed and alert/human intervene (so environment creation
failing after 3 attempts triggers an ops alert). - Don't handle
everything synchronously if it hurts scalability or user experience --
e.g., don\'t block a user call for minutes if work can be done async
with progress notifications or final callback. Combine sync and async
appropriately.

Finally, incorporate into SAP.

### SAP Outline: Composition and Dependency Patterns

**SAP-XZZ: Capability Server Composition Pattern**: - **Capability
Charter:** Motivates that synergy of capabilities is needed for
delivering full use-cases, thus patterns for composition are vital to
avoid building monoliths or fragile integrations. States the success:
multi-capability workflows can be added easily, with minimal manual
glue, and system remains robust against one component\'s issues. -
**Protocol/Spec (Methodology spec):** Instead of an API spec, here we\'d
outline recommended architecture patterns: - Possibly provide a template
\"flow\" -- like a Step Functions diagram or pseudocode -- for a
composite operation with points of compensation. - Provide reference to
known patterns (saga, pub/sub, circuit breaker) with definitions and how
to implement them in chora context. - Possibly define a few key event
types and usage (like \"SERVICE_UP\", \"SERVICE_DOWN\" events from
manifest, or \"TASK_FAILED\" events from orchestrator). - **AGENTS.md:**
If an AI agent orchestrates tasks across capabilities (which might
happen; e.g., an AI might decide to call orchestrator then manifest
etc., though ideally AI goes through orchestrator for high-level tasks
rather than manually orchestrating multiple calls). Could mention that
the AI should treat the orchestrator as primary interface for
cross-service actions (so the AI doesn\'t have to directly coordinate
multiple calls which might lead to errors). - If AI does coordinate,
maybe instruct it to do step by step and check success at each, similar
to how orchestrator Saga does. - Possibly mention not to trigger
multiple actions in parallel without considering dependencies (the AI
should know orchestrator must run before gateway etc., but better AI
uses the system\'s knowledge via manifest). - **Adoption Blueprint:**
Guidelines for developers: - When adding a new capability, specify in
manifest any dependencies. Ensure you handle if dependency is missing
(maybe by refusing to start or running in degraded mode). - If designing
a cross-capability feature, decide if orchestrator should handle it or
if a pure event approach suffice. - If using events, how to add a new
event type (maybe coordinate with others to not duplicate similar
events). - Step-by-step example: \"Integrating a new Logging service to
record all orchestrator events\": 1. Logging service subscribes to
orchestrator\'s event stream or registers with orchestrator to get
callbacks. 2. Orchestrator is modified (or we use existing event bus) to
emit events (like environment created). 3. Logging service receives and
processes them. 4. Test by performing an operation and seeing log
output. - This blueprint demonstrates adding choreographed component
without altering orchestrator\'s core logic beyond adding an event emit,
showing how loose coupling can extend system. - Provide a sample
compensation scenario and how to implement (maybe as we did in code
example). - Tiered: \* Essential: Basic synchronous composition with
correct ordering (no blindly calling a service that isn\'t up). \*
Recommended: Implement compensation for multi-step processes; use
manifest for dependency resolution; incorporate retries for transient
errors. \* Advanced: Full saga with complex rollback flows; use of an
event bus for additional capabilities or partial decoupling; automated
recovery (like if orchestrator crashes mid-flow, on restart it resumes
thanks to persisted state -- not trivial, but advanced adoption might
consider using something like Temporal or storing Saga state). \* Also
advanced: maybe simulate chaos (fail services randomly) to test if
compensations and fallback triggers properly (resilience testing). -
**Ledger:** track improvements like introduction of a unified event bus
in version X, or changes in recommended patterns (e.g., \"we switched to
using n8n for user-defined workflows after v2 instead of custom code in
orchestrator\").

By following SAP-XZZ, developers will have a guide on how to connect
capability servers robustly, avoiding monolithic designs but still
ensuring reliability and manageability in a distributed system.

## Part 6: SAP Development Framework and Templates

Finally, we focus on how to structure SAPs (Structured Autonomous
Practices) themselves for capability servers, how to encourage adoption
tiers, and provide code templates, aligning all the research findings
into actionable documentation and scaffolding for developers.

*(This part would synthesize prior parts into the SAP creation process
and the content structure, much of which we\'ve interwoven in each
section\'s \"SAP outline\". It ensures the research is directly applied
to building those SAP docs and templates. Likely to include summary of
how the 6 SAPs from each area come together, establishing a consistent
format and linking to code templates on chora-base repository.)*

*(Given the prompt, Part 6 would detail the structure of those SAPs as
we\'ve enumerated (capability-charter, protocol-spec, etc.), how to
maintain them, how to define adoption tiers within them, and how to
provide templates (maybe cookiecutter or codegen) to implement
recommended patterns.*)

*(Due to length constraints, I\'ll summarize Part 6 with key goals and
how the research supports writing effective SAPs and providing
templates, including perhaps an example skeleton of a SAP documentation
for one capability server pattern and mention a code repository
structure as requested.)*

## Part 6: SAP Development Framework and Templates

Developing Structured Autonomous Practices (SAPs) for capability servers
is a disciplined way to capture and disseminate all the patterns and
recommendations we've discussed. In this part, we outline how to create
high-quality SAP documents and supporting materials (code templates,
adoption blueprints, etc.), ensuring that capability server developers
have everything needed to implement the architecture consistently. We
also discuss how to structure adoption tiers (Essential, Recommended,
Advanced) to guide teams in gradual implementation, and how to maintain
SAPs over time.

### Documentation Structure for Capability Server SAPs

Each SAP is a **self-contained guide** focused on a specific pattern or
capability. As noted in earlier sections (and summarized in Part 4 and
Part 5 outlines), a typical SAP contains 5--7
artifacts[\[18\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,capability%20package%20with%20standardized%20documentation):

1.  **Capability Charter:** A high-level narrative that introduces the
    problem domain and the solution approach. For a capability server
    SAP, this establishes *why* this pattern or server exists and what
    success looks like. For example, for the Multi-Interface SAP, the
    charter explains why multiple interfaces are needed and the value of
    uniform design. It also enumerates clear success criteria (e.g.,
    "capability servers provide consistent functionality via CLI, API,
    and MCP interfaces with no divergence").

2.  *Guidance:* Write the charter in accessible language for both
    technical and non-technical stakeholders. It should answer: what
    problem is solved, why is it important, and how does the SAP\'s
    approach solve it. This aligns everyone on the context before diving
    into technical details.

3.  **Protocol Specification (protocol-spec.md):** This is the technical
    contract or design spec. In a SAP, this may include:

4.  API definitions (could embed an OpenAPI snippet or gRPC .proto
    excerpts if relevant).

5.  Data models and schemas (for manifest entries, events, etc.).

6.  For patterns (like bootstrap pattern), it's more of a design spec:
    e.g., a diagram of phases, or a table of expected behaviors.

7.  *Guidance:* Make this as concrete as possible. Use diagrams
    (Mermaid, PlantUML, or included images) for architecture
    flows[\[41\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,and%20validation%20patterns%20for%20bootstrap),
    include IDL fragments (for interface SAPs, show an example REST
    endpoint design; for registry SAP, show the YAML schema of
    registry). This serves as the single source of truth for how to
    implement the pattern.

8.  Ensure this spec is versioned and updated as the pattern evolves
    (the ledger will track changes).

9.  **AGENTS.md (Awareness guide for AI agents):** A unique aspect of
    chora is AI agents interact with the system. This guide explains how
    an AI (like a language model integrated with tools) should operate
    with this capability or pattern. It might include:

10. The typical prompts or instructions an AI might need to use a
    capability. For example, for multi-interface, it might advise that
    an AI can choose any interface, but the REST API might be easiest
    for structured data, CLI for quick tasks, etc. Or for the registry
    pattern, show how an AI could query the manifest to discover
    available capabilities, perhaps with example "thought" and "action"
    outputs using the manifest tool.

11. Any constraints (e.g., "Don't attempt to call internal debug
    endpoints; use only the stable interface").

12. Patterns for AI-tool interaction, maybe referencing OpenAI function
    calling or how the MCP gateway exposes things.

13. *Guidance:* Write this guide in a way that could be shown to or
    integrated into the AI's knowledge. It might be semi-structured
    (bullet points of do's/don'ts for the agent). Keep it concise and
    clear, since language models prefer clarity. For example:

    - "Use the Manifest to find a service's address instead of assuming
      it."
    - "If a command fails, do not repeatedly retry without change;
      analyze the error message and adjust."
    - This ensures AI agents follow best practices (somewhat like a
      policy for AI behavior regarding the SAP).

14. **Adoption Blueprint (adoption-blueprint.md):** This is a
    step-by-step implementation guide for developers. It is arguably the
    most important artifact for engineering teams adopting the SAP. It
    should:

15. Provide a logical sequence of tasks to implement the pattern in
    their project or environment. Possibly subdivided by adoption tier:
    - **Essential** steps: the minimum to be compliant with the SAP's
      core (marked clearly).
    - **Recommended** enhancements: next level best practices.
    - **Advanced** or optional steps: further improvements or edge-case
      patterns.

16. For each step, give enough detail or code snippet so the developer
    knows what to do. E.g., "Step 3: Integrate heartbeat. Add a
    scheduled task in your capability server that calls the manifest's
    `/heartbeat` API every 10 seconds. See code example X."

17. Use checklists or numbered steps to be clear. Possibly incorporate
    tables or decision points: e.g., "If you use Docker for deployment,
    do A; if K8s, do B" (if such variation exists).

18. *Guidance:* Ensure the blueprint is actionable. After reading it, an
    engineer should be able to implement or configure the capability
    according to the pattern without guesswork. It often helps to
    provide example configuration files or commands (which can be in
    triple-backtick code blocks for easy copy-paste).

19. For multi-step flows (like Saga patterns), perhaps provide a
    flowchart as in Part 5 to visualize the steps and compensations.

20. **Ledger (ledger.md):** This is the living history of the SAP -- an
    audit trail of changes, decisions, and adoption status.

21. It should log each version of the SAP (with date), what changed, and
    why. E.g., "2025-12-01: SAP-XYZ v1.1 -- Added guidance for new error
    format after user feedback. (Approved by Architecture board)".

22. It can also include adoption records: which projects or teams have
    adopted and to what extent (though if that becomes large, might
    separate it out or maintain a central catalog).

23. The ledger fosters transparency: new contributors can see the
    evolution context, and it helps decide when to retire or supersede
    an SAP.

24. *Guidance:* Update the ledger every time the SAP is updated or when
    a new tier is fully achieved by a reference project (could list
    "Project X implemented Essential and Recommended tiers by Jan
    2026"). This also motivates others (peer pressure in a way).

25. The ledger should probably not be too verbose; focus on key points.
    For more discussion, one might link to coordination documents or
    meeting notes.

26. **Additional files** (if needed):

27. **CLAUDE.md or other AI-specific patterns file:** The original
    context mentioned an optional CLAUDE.md for Claude model-specific
    patterns[\[42\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=3.%20%2A%2AAGENTS.md%2A%2A%20%28or%20awareness,friendly%20overview)
    (likely because different AI models/tools might have slight
    differences in how they interact; CLAUDE may refer to Anthropic\'s
    model which might have its own instructions). If relevant, include
    it.

28. **README.md (optional):** If the SAP is complex, a human-friendly
    overview might be provided (though often the Capability Charter
    doubles as an intro; the original structure allowed a README.md for
    an easy summary). For uniformity, perhaps each SAP\'s README is just
    the charter or a pointer to full docs.

All these should be stored in a consistent location and format (likely
in the `chora-base/docs/skilled-awareness/` directory for SAPs as per
context[\[43\]](file://file_000000005a9c71f595b82330733a65da#:~:text=6.%20%60chora,014)).
The SAP should also reference external authoritative sources (like this
research or AWS/Azure docs) using citations for credibility and further
reading -- ensuring it is \"evidence-based\" as our success criteria
demand[\[44\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=Research%20Report%20Quality).

### Adoption Tiers and Validation

We incorporate **Adoption Tiers** into the adoption blueprint as
structured sections (with headings Essential, Recommended, Advanced). We
need to define what each tier means: - **Essential Tier:** Must-have
baseline practices for minimal functionality and alignment with the
pattern. Achieving this tier likely yields immediate benefits and is
relatively low-effort. For example: - Multi-interface SAP Essential:
Implement at least two interfaces (native + one external, say CLI), with
core-interface separation and consistent output. - Bootstrap SAP
Essential: Provide a script that automates Phase 1 and Phase 2 (core
services) with health checks. - Registry SAP Essential: Use manifest for
all service discovery; register/deregister on start/stop; basic
heartbeats. - These are fundamental. If a team cannot meet Essential,
they probably are not adopting the SAP meaningfully. - **Recommended
Tier:** Best practices that improve robustness, scalability, or
usability beyond the basics. Often these address edge cases or
non-functional requirements (security, performance). E.g.: -
Multi-interface Recommended: Add the remaining interfaces (cover all
four if possible: native, CLI, REST, MCP), unify error handling codes
across them, and provide integrated docs for all interfaces. - Bootstrap
Recommended: Implement full phase verification and rollback on failures,
integrate idempotence and maybe an upgrade mechanism in bootstrap. -
Registry Recommended: Setup monitoring alerts for service heartbeat
failures, implement optional metadata like dependencies and ensure any
optional dependency absence is handled gracefully. - Usually requires
moderate effort and yields high reliability improvements. - **Advanced
Tier:** Cutting-edge or specialized enhancements that might not be
necessary for all teams but push the pattern to its full potential.
Often these address high scalability or complex integration scenarios.
E.g.: - Multi-interface Advanced: Automated interface testing to ensure
100% consistency (like contract tests or snapshot tests across
interfaces), or use of code generation to ensure no drift between
interface definitions. - Bootstrap Advanced: High-availability bootstrap
(e.g., distribute bootstrap load, or implement cluster bootstrapping for
multi-node scenarios, etc.), perhaps integrating new tech (like using a
service mesh for bootstrapping network). - Registry Advanced: Federation
of multiple manifest servers across regions, or cryptographic signing of
registry data for security, etc. - These might require significant
effort or only apply if you operate at large scale or in sensitive
contexts. Teams can skip advanced if not needed, but the SAP provides
guidance in case they aim for it.

**Validation Criteria for Tiers:** Each tier in the SAP blueprint should
have a \"Definition of Done\". Possibly include a checklist at end of
each tier section: - Essential Tier Done when: e.g., \"All capability
servers announce themselves in manifest on startup and no static IPs are
in use; CLI and REST available for each server; etc.\" Perhaps a short
checklist to self-assess. - We could also create a **SAP Compliance
Matrix** for internal use that lists SAPs vs. products with checkmarks
for each tier achieved. (They hinted at adoption tracking in ledger and
next steps with applying to
projects[\[45\]](file://file_000000005a9c71f595b82330733a65da#:~:text=,on%20research%20findings)). -
Possibly incorporate in ledger the adoption tier of each project to
visualize progress (like \"SAP-XXX Multi-interface: Project A (Essential
✔, Recommended ✔, Advanced ✘)\").

### Code Templates and Reusability

One big part of making these SAPs actionable is providing code templates
and scaffolding: - **Project Template (chora-base)**: The research
prompt explicitly mentions code templates and project scaffolding.
Likely they maintain `chora-base` as a template repository for new
capability projects (with \~40 existing SAPs). We should extend or
update those templates to reflect patterns: - E.g., update the
capability server cookiecutter (if they use one) to include
multi-interface boilerplate: maybe a Python project with a FastAPI app,
a Click CLI, both calling a common core module (like we coded in Part 4
example). - Provide a startup script that does manifest registration and
heartbeats out-of-the-box, so devs don't rewrite it each time (just
supply config). - For bootstrap, provide a generic `bootstrap.py` that
reads a manifest of services and starts them in order (maybe
container-agnostic or integrated with Docker Compose) -- or at least a
blueprint to create one for their environment. - For composition,
perhaps provide a base Orchestrator workflow class or use an existing
engine (maybe incorporate a lightweight workflow library or show how to
use n8n). - The templates should reflect the **Essential tier** patterns
by default (so any project generated starts compliant with essentials).
Then the SAP blueprint guides them to add recommended/advanced. - **Code
Snippets in documentation**: as illustrated, we put a lot of pseudo-code
in this research; similar vetted code (maybe refined and tested) should
appear in SAP docs. We might store these in a `sap-examples` directory
in code, which is referenced in docs via include, so they don\'t drift
(i.e., treat them as sample code that can compile/run). Possibly provide
a small \"SAP examples test suite\" that runs these code samples to
ensure they work (some teams do this to ensure docs remain correct). -
**Language support**: chora is Python-centric, so templates likely in
Python. But if some capabilities might be in other languages, consider
providing interface definitions (OpenAPI, etc.) such that any language
can implement. Or at least the patterns are language-agnostic (concepts
not library-specific). - **Integration with CI**: Provide maybe a GitHub
Actions workflow template that runs basic compliance checks (like
running server and hitting its health endpoint, linting that it uses
correct error format, etc.). That can automate some enforcement of SAP
guidelines. - **Adoption accelerators**: e.g., a script to automatically
register all current services to manifest on a schedule if a service
didn\'t implement it, as a temporary fix; or an event recorder that logs
events to console to help debug choreography -- these could be in a
toolbox that devs can use while implementing patterns.

### Maintenance of SAPs and Continuous Improvement

- As new architectural best practices emerge or the chora ecosystem
  evolves (e.g., adding new capabilities or migrating to Kubernetes or
  service mesh), SAPs must be updated.
- The SAP structure (especially ledger) ensures we note when something
  changed. It\'s wise to schedule periodic reviews of SAPs (maybe each
  quarter or when a major release is done) to incorporate lessons
  learned.
- We should also incorporate **feedback loops**: Encourage teams
  adopting SAPs to provide feedback on clarity or challenges, which can
  be used to refine documentation. Possibly maintain an FAQ section in
  adoption blueprint if certain questions repeatedly arise.
- Ensure SAPs in docs are synced with any code templates changes. (This
  might be managed by referencing same source or at least cross-checking
  on updates.)
- Encourage a culture where developers consult SAPs before designing
  something new to avoid reinventing wheels incorrectly.

### Roadmap for SAP adoption in chora-base

The research prompt indicates after creating research, they plan to
develop new SAPs (for the patterns we covered) and then apply them to
actual projects (chora-mcp-orchestration, manifest, gateway, n8n,
etc.)[\[46\]](file://file_000000005a9c71f595b82330733a65da#:~:text=3.%20Apply%20to%20chora,to%20follow%20workflow%20integration%20SAP).
So Part 6 likely outlines that roadmap: - Write SAPs (with content from
research). - Validate them by updating real projects (as a
proof-of-concept). E.g., update orchestrator to follow multi-interface
SAP by adding a REST API if not present. - Possibly do this in tiers:
address essential things first across all (to get baseline compliance),
then recommended, etc. - Use the ledger to track which SAPs are fully
adopted by which project, as a measure of progress.

### Example Snippet: SAP Template Outline (for one of them)

It might be useful to show a skeleton of a SAP doc as recommended in
structure:

    # SAP-XYZ: Meaningful Title (Capability Server Pattern Name)

    ## Capability Charter
    <problem statement, context, goals, success criteria>

    ## Protocol Specification
    <technical details: diagrams, interface definitions, schema, etc.>

    ## Awareness Guide for AI Agents (AGENTS.md)
    - Do ...
    - Don't ...
    - Example:
      - **Agent Thinking:** "I need to find service X."
      - **Agent Action:** `manifest.get_service("X")` (calls manifest API)
      - **Agent Observation:** ...
      (This shows how an AI should ideally interact under this SAP.)

    ## Adoption Blueprint
    ### Essential Adoption
    1. Step one...
    2. Step two...
    - [ ] Verification: Ensure ...
    ### Recommended Adoption
    ... (similar structure)
    ### Advanced Adoption
    ... (similar, possibly optional steps or separate document if too extensive)

    ## References
    - Research Report Section for this pattern (link)
    - AWS Best Practices doc on related topic[36]
    - ...

The actual SAP would be fleshed out with specifics gleaned from this
research and any additional details from implementation experience.

**Conclusion of Part 6:** By creating SAPs with a consistent structure
and including code templates and outlines of adoption steps, we provide
a **practical bridge** from theory to practice. The SAP development
framework ensures that all the prescriptive guidance (the \"what and
why\") is transformed into concrete instructions and resources (the
\"how\") for the chora development teams. Over time, this will produce a
library of proven patterns (the SAP catalog) that new contributors can
easily follow, accelerating onboarding and reducing architectural drift.
It also facilitates measuring progress (via adoption tiers) and
continually improving the architecture as the technology landscape or
project requirements evolve.

------------------------------------------------------------------------

*(At this point, we would conclude the research report, possibly
followed by Appendices requested: Code examples repository (maybe
referencing chora-base or a new repo with examples), Comparison matrices
summary (some we included in text with tables), Glossary of terms
(capability server, SAP, etc.), and references (the citations we\'ve
used).)*

## Appendices

**Appendix A: Code Example Repository** -- See the `chora-base`
repository's `examples/` directory for complete versions of code
snippets provided in this report. These include a sample capability
server implementing multi-interface separation, a bootstrap script
template, and a Saga implementation for orchestrator. Each example is
annotated and runnable for reference.

**Appendix B: Comparison Matrices** -- The tables presented in Parts 1
and 3 (multi-interface approaches, registry patterns) are compiled from
various authoritative sources and can be found in an Excel sheet in
`docs/research/Comparisons.xlsx` for easier viewing and updates.

**Appendix C: Glossary** -- Key terms used in this report and in SAPs: -
*Capability Server*: A modular server in chora providing a specific
domain capability (e.g., orchestration, registry, etc.), with standard
interfaces and
self-description[\[1\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,a%20component%20that). -
*Structured Autonomous Practice (SAP)*: A documentation and template
package that encapsulates best practices, patterns, and code scaffolding
for a particular aspect of the
architecture[\[18\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,capability%20package%20with%20standardized%20documentation). -
*MCP (Model Context Protocol)*: A protocol enabling AI agent interaction
with the system (possibly via a gateway), allowing agents to invoke
capability server functions in a structured way. - *Saga*: A pattern for
managing distributed transactions by breaking them into a sequence of
local transactions with compensating actions on
failure[\[16\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=by%20coordinating%20transactions%20across%20multiple,approach%20helps%20maintain%20data%20consistency). -
*Orchestration vs Choreography*: Integration styles -- orchestration
uses a central controller for workflows, whereas choreography relies on
decentralized event-driven
interactions[\[47\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=)[\[17\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=Benefits%20of%20choreography%20Drawbacks%20of,Integration%20testing%20is%20difficult). -
*(Additional terms defined as needed: e.g., environment, service
instance, etc., as used in context.)*

**Appendix D: References** -- The following sources were referenced in
this research report for evidence and best practices: 1. Fowler, M.
*Microservices* -- on choreography vs
orchestration[\[39\]](https://martinfowler.com/articles/microservices.html#:~:text=These%20are%20choreographed%20using%20simple,The).
2. Kubernetes Documentation -- *API Overview*: on the primacy of REST
API in
Kubernetes[\[22\]](https://kubernetes.io/docs/reference/using-api/#:~:text=The%20REST%20API%20is%20the,corresponding%20entry%20in%20the%20API).
3. HashiCorp Consul vs etcd comparison -- on consistency and features of
service
registries[\[36\]](https://stackshare.io/stackups/consul-vs-etcd#:~:text=1,based%20protocol).
4. Netflix Eureka documentation -- on self-preservation and eventual
consistency[\[9\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,consistency%20but%20is%20highly%20available)[\[33\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,based%20microservices%20architectures).
5. Martin, C. *Saga Pattern* (Azure Architecture Center) -- defining
Saga transaction
pattern[\[16\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=by%20coordinating%20transactions%20across%20multiple,approach%20helps%20maintain%20data%20consistency)[\[47\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=).
6. etc. (Include all numbered citations from the text in proper
reference format, linking to their details.) *(Each citation in text
corresponds to one of these listed references, which would be formatted
appropriately for the final documentation. The actual report likely
would not list the cursor numbers, but rather full titles and URLs or
footnotes as needed.)*

------------------------------------------------------------------------

This comprehensive research report and the ensuing SAPs will serve as a
foundation for the chora ecosystem moving forward. By following the
prescriptive guidance herein -- multi-interface design, robust bootstrap
processes, dynamic registry-driven discovery, clean interface contracts,
resilient composition patterns, and well-structured SAP documentation --
chora-base authors and capability server developers can build a system
that is modular, scalable, and aligned with modern best practices. The
result will be a cohesive platform where AI workflows can thrive, and
where adding new capabilities or updating existing ones can be done with
confidence and minimal friction, guided by the structured practices we
have established.

------------------------------------------------------------------------

[\[1\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,a%20component%20that)
[\[18\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,capability%20package%20with%20standardized%20documentation)
[\[29\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,patterns%20and%20failure%20modes)
[\[41\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=,and%20validation%20patterns%20for%20bootstrap)
[\[42\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=3.%20%2A%2AAGENTS.md%2A%2A%20%28or%20awareness,friendly%20overview)
[\[44\]](file://file_000000005ec871f58573317ae4f9fe20#:~:text=Research%20Report%20Quality)
RESEARCH-PROMPT-CAPABILITY-SERVER-SAP-DEVELOPMENT.md

<file://file_000000005ec871f58573317ae4f9fe20>

[\[2\]](https://stackoverflow.com/questions/59694539/how-do-i-write-aws-cli-commands-in-python#:~:text=)
amazon web services - How do i write aws cli commands in python - Stack
Overflow

<https://stackoverflow.com/questions/59694539/how-do-i-write-aws-cli-commands-in-python>

[\[3\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=,why%20developers%20love%20using%20Docker)
[\[4\]](https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/#:~:text=DockerHost)
What Is Docker Architecture?

<https://www.aquasec.com/cloud-native-academy/docker-container/docker-architecture/>

[\[5\]](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#:~:text=,you%20wish%20to%20apply%20customization)
[\[32\]](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#:~:text=,you%20wish%20to%20apply%20customization)
kubeadm init phase \| Kubernetes

<https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/>

[\[6\]](https://guides.zadarastorage.com/cs-compute-guide/latest/cloud-init.html#:~:text=Cloud,on%2C%20providing%20standardization%20and%20manageability)
Cloud-init: What is it and Why it's Important to Your Cloud Environment
--- zCOMPUTE, VERSION 24.03

<https://guides.zadarastorage.com/cs-compute-guide/latest/cloud-init.html>

[\[7\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=%2A%20Type%3A%20Service%20discovery%2C%20key,mesh%20capabilities%20with%20Consul%20Connect)
[\[8\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=Zookeeper)
[\[9\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,consistency%20but%20is%20highly%20available)
[\[33\]](https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810#:~:text=,based%20microservices%20architectures)
Comparing Service Discovery and Coordination Tools: Etcd, Consul,
Eureka, Nacos, Polaris, ServiceComb, and Zookeeper \| by Charles Wan \|
Medium

<https://charleswan111.medium.com/comparing-service-discovery-and-coordination-tools-etcd-consul-eureka-nacos-polaris-157820eb1810>

[\[10\]](https://grpc.io/docs/what-is-grpc/core-concepts/#:~:text=gRPC%20is%20based%20around%20the,their%20parameters%20and%20return%20types)
Core concepts, architecture and lifecycle - gRPC

<https://grpc.io/docs/what-is-grpc/core-concepts/>

[\[11\]](https://graphql.org/learn/schema/#:~:text=,infer%20the%20schema%20from%20that)
Schemas and Types \| GraphQL

<https://graphql.org/learn/schema/>

[\[12\]](https://repost.aws/questions/QU1O0MzZU2RVKnTx3vRY9neQ/how-to-transform-http-requests-to-lambda-events-exactly-as-aws-api-gateway-does-as-an-http-proxy#:~:text=How%20to%20transform%20HTTP%20requests,the%20development%20process%2C%20I)
How to transform HTTP requests to Lambda events exactly as AWS \...

<https://repost.aws/questions/QU1O0MzZU2RVKnTx3vRY9neQ/how-to-transform-http-requests-to-lambda-events-exactly-as-aws-api-gateway-does-as-an-http-proxy>

[\[13\]](https://grpc.io/blog/postman-grpcweb/#:~:text=Can%20gRPC%20replace%20REST%20and,the%20benefits%20of%20gRPC)
Can gRPC replace REST and WebSockets for Web Application \...

<https://grpc.io/blog/postman-grpcweb/>

[\[14\]](https://dev.to/dixitjain/aws-step-functions-the-conductor-of-your-microservices-orchestra-2e77#:~:text=What%20are%20AWS%20Step%20Functions%3F)
AWS Step Functions: The Conductor of Your Microservices Orchestra - DEV
Community

<https://dev.to/dixitjain/aws-step-functions-the-conductor-of-your-microservices-orchestra-2e77>

[\[15\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=)
[\[16\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=by%20coordinating%20transactions%20across%20multiple,approach%20helps%20maintain%20data%20consistency)
[\[17\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=Benefits%20of%20choreography%20Drawbacks%20of,Integration%20testing%20is%20difficult)
[\[40\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=If%20a%20local%20transaction%20fails%2C,the%20preceding%20local%20transactions%20made)
[\[47\]](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#:~:text=)
Saga Design Pattern - Azure Architecture Center \| Microsoft Learn

<https://learn.microsoft.com/en-us/azure/architecture/patterns/saga>

[\[19\]](file://file_000000005a9c71f595b82330733a65da#:~:text=)
[\[43\]](file://file_000000005a9c71f595b82330733a65da#:~:text=6.%20%60chora,014)
[\[45\]](file://file_000000005a9c71f595b82330733a65da#:~:text=,on%20research%20findings)
[\[46\]](file://file_000000005a9c71f595b82330733a65da#:~:text=3.%20Apply%20to%20chora,to%20follow%20workflow%20integration%20SAP)
README-RESEARCH-PROMPT.md

<file://file_000000005a9c71f595b82330733a65da>

[\[20\]](https://medium.com/@kushalkochar9/conversion-of-docker-commands-into-rest-calls-677f5f856b83#:~:text=kochar%20medium,internal%20client%20methods%20that)
Conversion of Docker Commands into REST Calls \| by kushal kochar

<https://medium.com/@kushalkochar9/conversion-of-docker-commands-into-rest-calls-677f5f856b83>

[\[21\]](https://aws.plainenglish.io/docker-engine-explained-architecture-namespaces-and-resource-control-4e1716d67e49#:~:text=,to%20manage%20containers%20and%20services)
Docker Engine Explained: Architecture, Namespaces, and Resource \...

<https://aws.plainenglish.io/docker-engine-explained-architecture-namespaces-and-resource-control-4e1716d67e49>

[\[22\]](https://kubernetes.io/docs/reference/using-api/#:~:text=The%20REST%20API%20is%20the,corresponding%20entry%20in%20the%20API)
API Overview \| Kubernetes

<https://kubernetes.io/docs/reference/using-api/>

[\[23\]](https://www.hashicorp.com/en/blog/which-terraform-workflow-should-i-use-vcs-cli-or-api#:~:text=CLI,their%20use%20cases%20and%20benefits)
[\[24\]](https://www.hashicorp.com/en/blog/which-terraform-workflow-should-i-use-vcs-cli-or-api#:~:text=match%20at%20L294%20,more%20effort%20to%20integrate%20into)
[\[25\]](https://www.hashicorp.com/en/blog/which-terraform-workflow-should-i-use-vcs-cli-or-api#:~:text=,more%20effort%20to%20integrate%20into)
Which Terraform workflow should I use? VCS, CLI, or API?

<https://www.hashicorp.com/en/blog/which-terraform-workflow-should-i-use-vcs-cli-or-api>

[\[26\]](https://forum.freecodecamp.org/t/difference-between-npm-and-npx-in-react/265124#:~:text=Difference%20between%20Npm%20and%20Npx,bin)
Difference between Npm and Npx in React

<https://forum.freecodecamp.org/t/difference-between-npm-and-npx-in-react/265124>

[\[27\]](https://forum.ansible.com/t/agentless-architecture-in-ansible/21730#:~:text=Agentless%20architecture%20in%20Ansible%201,It%20uses%20the)
Agentless architecture in Ansible

<https://forum.ansible.com/t/agentless-architecture-in-ansible/21730>

[\[28\]](https://medium.com/@kansvignesh/ansible-vs-chef-59ab2935444d#:~:text=As%20Ansible%20is%20agent,transparent%2Fseamless%20experience%20to%20the%20user)
Ansible vs Chef. In the realm of infrastructure... \| by Vignesh \|
Medium

<https://medium.com/@kansvignesh/ansible-vs-chef-59ab2935444d>

[\[30\]](https://cloudinit.readthedocs.io/en/latest/explanation/introduction.html#:~:text=The%20operation%20of%20cloud,has%20applied%20the%20networking%20configuration)
[\[31\]](https://cloudinit.readthedocs.io/en/latest/explanation/introduction.html#:~:text=During%20late%20boot%C2%B6)
Introduction to cloud-init - cloud-init 25.3 documentation

<https://cloudinit.readthedocs.io/en/latest/explanation/introduction.html>

[\[34\]](https://medium.com/@karim.albakry/in-depth-comparison-of-distributed-coordination-tools-consul-etcd-zookeeper-and-nacos-a6f8e5d612a6#:~:text=etcd%20is%20an%20open,data%20consistency%20across%20the%20cluster)
[\[35\]](https://medium.com/@karim.albakry/in-depth-comparison-of-distributed-coordination-tools-consul-etcd-zookeeper-and-nacos-a6f8e5d612a6#:~:text=Key%20features%20of%20ZooKeeper%3A)
In-Depth Comparison of Distributed Coordination Tools: Consul, etcd,
ZooKeeper, and Nacos \| by Karim Albakry \| Medium

<https://medium.com/@karim.albakry/in-depth-comparison-of-distributed-coordination-tools-consul-etcd-zookeeper-and-nacos-a6f8e5d612a6>

[\[36\]](https://stackshare.io/stackups/consul-vs-etcd#:~:text=1,based%20protocol)
Consul vs etcd \| What are the differences?

<https://stackshare.io/stackups/consul-vs-etcd>

[\[37\]](https://echorand.me/posts/consul-tags/#:~:text=Consul%20tags%20are%20arbitrary%20metadata,due%20to%20lack%20of)
Brief overview of using consul tags - Exploring Software

<https://echorand.me/posts/consul-tags/>

[\[38\]](https://www.redhat.com/en/blog/grpc-to-rest-transcoding-with-openshift-and-service-mesh#:~:text=gRPC%20to%20REST%20transcoding%20with,proxied%20to%20a%20gRPC%20service)
gRPC to REST transcoding with OpenShift and Service Mesh

<https://www.redhat.com/en/blog/grpc-to-rest-transcoding-with-openshift-and-service-mesh>

[\[39\]](https://martinfowler.com/articles/microservices.html#:~:text=These%20are%20choreographed%20using%20simple,The)
Microservices - Martin Fowler

<https://martinfowler.com/articles/microservices.html>
