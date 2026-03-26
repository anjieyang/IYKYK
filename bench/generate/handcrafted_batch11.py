"""Hand-crafted batch 11 — ~500 unique cases for LLM router classifier.

Strategy:
- NEW domains: compiler design, operating systems, network protocols, database internals,
  distributed consensus, real-time systems, signal processing, robotics kinematics,
  computational geometry, graph algorithms, type theory, category theory
- Focus: more COMPLEX and REASONING (boost underrepresented tiers)
- Adversarial: coding questions that are SIMPLE (what does code do), proofs that look like
  explanations, system designs that are actually MEDIUM (single component)
- 14+ languages, English ~35%, boost non-English
- Zero overlap with batches 1–10
"""

from __future__ import annotations


def _c(prompt: str, tier: str, cat: str, lang: str) -> dict:
    return {"prompt": prompt, "expected_tier": tier, "category": cat, "lang": lang}


# ═══════════════════════════════════════════════════════════
#  SIMPLE (~140)
# ═══════════════════════════════════════════════════════════

SIMPLE_B11: list[dict] = [
    # ── Compiler design factual ──
    _c("What is a lexer?", "SIMPLE", "factual-qa", "en"),
    _c("What is an abstract syntax tree?", "SIMPLE", "factual-qa", "en"),
    _c("What does LLVM stand for?", "SIMPLE", "factual-qa", "en"),
    _c("What is register allocation?", "SIMPLE", "factual-qa", "en"),
    _c("What is constant folding?", "SIMPLE", "factual-qa", "en"),
    _c("What is a symbol table?", "SIMPLE", "factual-qa", "en"),
    # ── Operating systems factual ──
    _c("What is a page fault?", "SIMPLE", "factual-qa", "en"),
    _c("What is the difference between a process and a thread?", "SIMPLE", "factual-qa", "en"),
    _c("What is a semaphore?", "SIMPLE", "factual-qa", "en"),
    _c("What is virtual memory?", "SIMPLE", "factual-qa", "en"),
    _c("What is the kernel?", "SIMPLE", "factual-qa", "en"),
    _c("What is a context switch?", "SIMPLE", "factual-qa", "en"),
    _c("What is a TLB?", "SIMPLE", "factual-qa", "en"),
    # ── Network protocols factual ──
    _c("What port does HTTPS use?", "SIMPLE", "factual-qa", "en"),
    _c("What is the difference between TCP and UDP?", "SIMPLE", "factual-qa", "en"),
    _c("What is BGP?", "SIMPLE", "factual-qa", "en"),
    _c("What is OSPF?", "SIMPLE", "factual-qa", "en"),
    _c("What is a MAC address?", "SIMPLE", "factual-qa", "en"),
    _c("What is the three-way handshake?", "SIMPLE", "factual-qa", "en"),
    _c("What is QUIC?", "SIMPLE", "factual-qa", "en"),
    _c("What is the difference between IPv4 and IPv6?", "SIMPLE", "factual-qa", "en"),
    # ── Database internals factual ──
    _c("What is a B-tree?", "SIMPLE", "factual-qa", "en"),
    _c("What is WAL?", "SIMPLE", "factual-qa", "en"),
    _c("What is MVCC?", "SIMPLE", "factual-qa", "en"),
    _c("What is a checkpoint in databases?", "SIMPLE", "factual-qa", "en"),
    _c("What is an LSM tree?", "SIMPLE", "factual-qa", "en"),
    _c("What is the difference between clustered and non-clustered indexes?", "SIMPLE", "factual-qa", "en"),
    _c("What is ACID?", "SIMPLE", "factual-qa", "en"),
    # ── Distributed consensus factual ──
    _c("What is the Raft algorithm?", "SIMPLE", "factual-qa", "en"),
    _c("What is Paxos?", "SIMPLE", "factual-qa", "en"),
    _c("What is a quorum?", "SIMPLE", "factual-qa", "en"),
    _c("What is leader election?", "SIMPLE", "factual-qa", "en"),
    _c("What is the two-phase commit protocol?", "SIMPLE", "factual-qa", "en"),
    _c("What is eventual consistency?", "SIMPLE", "factual-qa", "en"),
    _c("What is a split brain?", "SIMPLE", "factual-qa", "en"),
    # ── Real-time systems factual ──
    _c("What is a hard real-time system?", "SIMPLE", "factual-qa", "en"),
    _c("What is EDF scheduling?", "SIMPLE", "factual-qa", "en"),
    _c("What is a worst-case execution time?", "SIMPLE", "factual-qa", "en"),
    _c("What is rate monotonic scheduling?", "SIMPLE", "factual-qa", "en"),
    _c("What is jitter?", "SIMPLE", "factual-qa", "en"),
    _c("What is a deadline miss?", "SIMPLE", "factual-qa", "en"),
    _c("What is priority inversion?", "SIMPLE", "factual-qa", "en"),
    _c("What is a sporadic task?", "SIMPLE", "factual-qa", "en"),
    # ── Signal processing / robotics / geometry factual ──
    _c("What is the Nyquist rate?", "SIMPLE", "factual-qa", "en"),
    _c("What is the FFT?", "SIMPLE", "factual-qa", "en"),
    _c("What is a convolution?", "SIMPLE", "factual-qa", "en"),
    _c("What is the Jacobian matrix in robotics?", "SIMPLE", "factual-qa", "en"),
    _c("What is forward kinematics?", "SIMPLE", "factual-qa", "en"),
    _c("What is inverse kinematics?", "SIMPLE", "factual-qa", "en"),
    _c("What is a convex hull?", "SIMPLE", "factual-qa", "en"),
    _c("What is a Voronoi diagram?", "SIMPLE", "factual-qa", "en"),
    # ── Type theory / category theory factual ──
    _c("What is a monad in programming?", "SIMPLE", "factual-qa", "en"),
    _c("What is a functor in category theory?", "SIMPLE", "factual-qa", "en"),
    _c("What is a type constructor?", "SIMPLE", "factual-qa", "en"),
    _c("What is structural typing?", "SIMPLE", "factual-qa", "en"),
    _c("What is a dependent type?", "SIMPLE", "factual-qa", "en"),
    _c("What is a natural transformation?", "SIMPLE", "factual-qa", "en"),
    _c("What is a product type?", "SIMPLE", "factual-qa", "en"),
    # ── Definitions / translations / greetings ──
    _c("Define lexical analysis", "SIMPLE", "definition", "en"),
    _c("What is a control flow graph?", "SIMPLE", "definition", "en"),
    _c("Translate 'compiler' to Vietnamese", "SIMPLE", "translation", "en"),
    _c("How do you say 'algorithm' in Turkish?", "SIMPLE", "translation", "en"),
    _c("Translate 'database' to Polish", "SIMPLE", "translation", "en"),
    _c("How do you say 'network' in Hindi?", "SIMPLE", "translation", "en"),
    _c("Hello", "SIMPLE", "greeting", "en"),
    _c("Good evening", "SIMPLE", "greeting", "en"),
    _c("Thanks", "SIMPLE", "greeting", "en"),
    # ── Adversarial: coding question that is SIMPLE (what does code do) ──
    _c("What does this code return? ```python\nx = [1,2,3]\nprint(x[-1])\n```", "SIMPLE", "code-snippet-qa", "en"),
    _c("What does `git merge --no-ff` do?", "SIMPLE", "factual-qa", "en"),
    _c("What does `chmod 755` set the permissions to?", "SIMPLE", "factual-qa", "en"),
    _c("What does `SELECT * FROM t LIMIT 10` return?", "SIMPLE", "factual-qa", "en"),
    _c("What does the `head -n 5` command do?", "SIMPLE", "factual-qa", "en"),
    _c("What does `std::move` do in C++?", "SIMPLE", "factual-qa", "en"),
    _c("What does `await` do in JavaScript?", "SIMPLE", "factual-qa", "en"),
    _c("What does `panic!` do in Rust?", "SIMPLE", "factual-qa", "en"),
    # ── Chinese ──
    _c("什么是词法分析器？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是抽象语法树？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是页错误？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 B 树？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 Raft 算法？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是前向运动学？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是单子？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 WAL？", "SIMPLE", "factual-qa", "zh"),
    _c("什么是 MVCC？", "SIMPLE", "factual-qa", "zh"),
    _c("你好", "SIMPLE", "greeting", "zh"),
    # ── Japanese ──
    _c("レキサーとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("抽象構文木とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("ページフォルトとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("B木とは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("Raftアルゴリズムとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("モナドとは何ですか？", "SIMPLE", "factual-qa", "ja"),
    _c("こんにちは", "SIMPLE", "greeting", "ja"),
    # ── Korean ──
    _c("렉서란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("추상 구문 트리란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("페이지 폴트란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("B-트리란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("Raft 알고리즘이란 무엇인가요?", "SIMPLE", "factual-qa", "ko"),
    _c("안녕하세요", "SIMPLE", "greeting", "ko"),
    # ── Arabic ──
    _c("ما هو المحلل المعجمي؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هي شجرة البنية المجردة؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هو خطأ الصفحة؟", "SIMPLE", "factual-qa", "ar"),
    _c("ما هي شجرة B؟", "SIMPLE", "factual-qa", "ar"),
    _c("مرحبا", "SIMPLE", "greeting", "ar"),
    # ── Russian ──
    _c("Что такое лексер?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое абстрактное синтаксическое дерево?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое страничный сбой?", "SIMPLE", "factual-qa", "ru"),
    _c("Что такое B-дерево?", "SIMPLE", "factual-qa", "ru"),
    _c("Привет", "SIMPLE", "greeting", "ru"),
    # ── Spanish ──
    _c("¿Qué es un lexer?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un árbol de sintaxis abstracta?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un fallo de página?", "SIMPLE", "factual-qa", "es"),
    _c("¿Qué es un árbol B?", "SIMPLE", "factual-qa", "es"),
    _c("Hola", "SIMPLE", "greeting", "es"),
    # ── German ──
    _c("Was ist ein Lexer?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein abstrakter Syntaxbaum?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein Seitenfehler?", "SIMPLE", "factual-qa", "de"),
    _c("Was ist ein B-Baum?", "SIMPLE", "factual-qa", "de"),
    _c("Hallo", "SIMPLE", "greeting", "de"),
    # ── French ──
    _c("Qu'est-ce qu'un lexer ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un arbre de syntaxe abstraite ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un défaut de page ?", "SIMPLE", "factual-qa", "fr"),
    _c("Qu'est-ce qu'un arbre B ?", "SIMPLE", "factual-qa", "fr"),
    _c("Bonjour", "SIMPLE", "greeting", "fr"),
    # ── Portuguese ──
    _c("O que é um lexer?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é uma árvore de sintaxe abstrata?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é um page fault?", "SIMPLE", "factual-qa", "pt"),
    _c("O que é uma árvore B?", "SIMPLE", "factual-qa", "pt"),
    _c("Olá", "SIMPLE", "greeting", "pt"),
    # ── Hindi ──
    _c("लेक्सर क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("अमूर्त वाक्यविन्यास वृक्ष क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("पेज फॉल्ट क्या है?", "SIMPLE", "factual-qa", "hi"),
    _c("नमस्ते", "SIMPLE", "greeting", "hi"),
    # ── Turkish ──
    _c("Lexer nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Soyut sözdizimi ağacı nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Sayfa hatası nedir?", "SIMPLE", "factual-qa", "tr"),
    _c("Merhaba", "SIMPLE", "greeting", "tr"),
    # ── Vietnamese ──
    _c("Lexer là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Cây cú pháp trừu tượng là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Lỗi trang là gì?", "SIMPLE", "factual-qa", "vi"),
    _c("Xin chào", "SIMPLE", "greeting", "vi"),
    # ── Polish ──
    _c("Co to jest lekser?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest drzewo składni abstrakcyjnej?", "SIMPLE", "factual-qa", "pl"),
    _c("Co to jest błąd strony?", "SIMPLE", "factual-qa", "pl"),
    _c("Cześć", "SIMPLE", "greeting", "pl"),
]


# ═══════════════════════════════════════════════════════════
#  MEDIUM (~180)
# ═══════════════════════════════════════════════════════════

MEDIUM_B11: list[dict] = [
    # ── Compiler design single-task ──
    _c("Write a recursive descent parser for a simple arithmetic expression grammar", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple lexer that tokenizes identifiers, numbers, and operators", "MEDIUM", "simple-code", "en"),
    _c("Write a function to perform constant folding on an AST node", "MEDIUM", "simple-code", "en"),
    _c("Implement a basic block builder that partitions a CFG into blocks", "MEDIUM", "simple-code", "en"),
    _c("Create a symbol table with scoping support for a toy language", "MEDIUM", "simple-code", "en"),
    _c("Write a simple register allocator using graph coloring for a small IR", "MEDIUM", "simple-code", "en"),
    _c("Implement a visitor pattern for traversing and transforming an AST", "MEDIUM", "simple-code", "en"),
    _c("Write a function to convert infix expressions to postfix (RPN)", "MEDIUM", "simple-code", "en"),
    _c("Implement dead code elimination for a simple three-address IR", "MEDIUM", "simple-code", "en"),
    _c("Create a simple type checker for a language with integers and booleans", "MEDIUM", "simple-code", "en"),
    # ── Operating systems single-task ──
    _c("Implement a simple round-robin scheduler in C", "MEDIUM", "simple-code", "en"),
    _c("Write a producer-consumer solution using semaphores", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple page replacement algorithm (FIFO or LRU)", "MEDIUM", "simple-code", "en"),
    _c("Write a function to simulate a context switch between two processes", "MEDIUM", "simple-code", "en"),
    _c("Implement a readers-writers lock with writer preference", "MEDIUM", "simple-code", "en"),
    _c("Create a simple memory allocator with first-fit strategy", "MEDIUM", "simple-code", "en"),
    _c("Write a shell script that monitors process CPU usage and kills top consumers", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple inode-based file system in userspace", "MEDIUM", "simple-code", "en"),
    _c("Write a program to demonstrate priority inversion and its fix", "MEDIUM", "simple-code", "en"),
    _c("Create a simple deadlock detection algorithm for a resource allocation graph", "MEDIUM", "simple-code", "en"),
    # ── Network protocols single-task ──
    _c("Implement a simple TCP client that connects and sends a message", "MEDIUM", "simple-code", "en"),
    _c("Write a function to parse an IPv4 packet header", "MEDIUM", "simple-code", "en"),
    _c("Implement a basic HTTP/1.1 request parser", "MEDIUM", "simple-code", "en"),
    _c("Create a simple DNS resolver that queries A records", "MEDIUM", "simple-code", "en"),
    _c("Write a UDP echo server with timeout handling", "MEDIUM", "simple-code", "en"),
    _c(
        "Implement subnet calculation: given IP and CIDR, return network and broadcast addresses",
        "MEDIUM",
        "simple-code",
        "en",
    ),
    _c("Write a function to validate and parse a MAC address string", "MEDIUM", "simple-code", "en"),
    _c("Create a simple ARP cache with TTL-based expiration", "MEDIUM", "simple-code", "en"),
    _c("Implement a basic TLS certificate chain validator", "MEDIUM", "simple-code", "en"),
    _c("Write a program to trace the route (traceroute) to a host", "MEDIUM", "simple-code", "en"),
    # ── Database internals single-task ──
    _c("Implement a B-tree insert operation", "MEDIUM", "simple-code", "en"),
    _c("Write a WAL redo pass that replays committed transactions", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple buffer pool with LRU eviction", "MEDIUM", "simple-code", "en"),
    _c("Create a hash index for equality lookups", "MEDIUM", "simple-code", "en"),
    _c("Write a function to compute the selectivity of a predicate for query planning", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple two-phase locking protocol", "MEDIUM", "simple-code", "en"),
    _c("Create a merge sort for external sorting of large relations", "MEDIUM", "simple-code", "en"),
    _c("Write a checkpoint routine that flushes dirty pages and truncates WAL", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple LSM compaction strategy", "MEDIUM", "simple-code", "en"),
    _c("Create a query plan cost estimator for nested loop and hash joins", "MEDIUM", "simple-code", "en"),
    # ── Graph algorithms single-task ──
    _c("Implement Kruskal's algorithm for minimum spanning tree", "MEDIUM", "simple-code", "en"),
    _c("Write a function to detect cycles in a directed graph using DFS", "MEDIUM", "simple-code", "en"),
    _c("Implement topological sort using Kahn's algorithm", "MEDIUM", "simple-code", "en"),
    _c(
        "Write a function to find strongly connected components using Tarjan's algorithm", "MEDIUM", "simple-code", "en"
    ),
    _c("Implement Bellman-Ford for shortest paths with negative edges", "MEDIUM", "simple-code", "en"),
    _c("Create a function to compute the maximum flow using Ford-Fulkerson", "MEDIUM", "simple-code", "en"),
    _c("Write a function to find articulation points in an undirected graph", "MEDIUM", "simple-code", "en"),
    _c("Implement Prim's algorithm for MST", "MEDIUM", "simple-code", "en"),
    _c("Write a function to compute all-pairs shortest paths with Floyd-Warshall", "MEDIUM", "simple-code", "en"),
    _c("Implement a bipartite matching algorithm", "MEDIUM", "simple-code", "en"),
    # ── Signal processing / geometry single-task ──
    _c("Implement a discrete Fourier transform (DFT) in Python", "MEDIUM", "simple-code", "en"),
    _c("Write a function to compute the convex hull of a set of points (Graham scan)", "MEDIUM", "simple-code", "en"),
    _c("Implement line segment intersection detection", "MEDIUM", "simple-code", "en"),
    _c("Write a function to compute the Jacobian for a 2-DOF robot arm", "MEDIUM", "simple-code", "en"),
    _c("Implement forward kinematics for a 2-link planar robot", "MEDIUM", "simple-code", "en"),
    _c("Create a simple low-pass filter (moving average or exponential)", "MEDIUM", "simple-code", "en"),
    _c("Write a function to downsample a signal by a factor N", "MEDIUM", "simple-code", "en"),
    _c("Implement point-in-polygon test using ray casting", "MEDIUM", "simple-code", "en"),
    _c("Write a function to compute the closest pair of points in O(n log n)", "MEDIUM", "simple-code", "en"),
    _c("Implement a simple Kalman filter for 1D position estimation", "MEDIUM", "simple-code", "en"),
    # ── Explanations ──
    _c("Explain how a compiler transforms source code to machine code", "MEDIUM", "explanation", "en"),
    _c("How does virtual memory mapping work with page tables?", "MEDIUM", "explanation", "en"),
    _c("Explain how TCP congestion control (AIMD) works", "MEDIUM", "explanation", "en"),
    _c("How does a database execute a query with a hash join?", "MEDIUM", "explanation", "en"),
    _c("Explain how Raft achieves consensus in the presence of failures", "MEDIUM", "explanation", "en"),
    _c("How does EDF scheduling guarantee schedulability?", "MEDIUM", "explanation", "en"),
    _c("Explain how the FFT reduces DFT complexity from O(n²) to O(n log n)", "MEDIUM", "explanation", "en"),
    _c("How does inverse kinematics solve for joint angles given end-effector pose?", "MEDIUM", "explanation", "en"),
    _c("Explain how Dijkstra's algorithm finds shortest paths", "MEDIUM", "explanation", "en"),
    _c("How does a monad enforce sequencing in functional programming?", "MEDIUM", "explanation", "en"),
    # ── Comparisons ──
    _c("Compare LL(1) vs LR parsing: when to use which?", "MEDIUM", "comparison", "en"),
    _c("Compare preemptive vs nonpreemptive scheduling for real-time systems", "MEDIUM", "comparison", "en"),
    _c("Compare TCP vs UDP for streaming applications", "MEDIUM", "comparison", "en"),
    _c("Compare B-tree vs LSM tree for write-heavy workloads", "MEDIUM", "comparison", "en"),
    _c("Compare Raft vs Paxos: pros and cons", "MEDIUM", "comparison", "en"),
    _c("Compare rate monotonic vs EDF for periodic task sets", "MEDIUM", "comparison", "en"),
    _c("Compare DFT vs FFT: when is FFT applicable?", "MEDIUM", "comparison", "en"),
    _c("Compare structural vs nominal typing", "MEDIUM", "comparison", "en"),
    _c("Compare functor vs monad: what can each express?", "MEDIUM", "comparison", "en"),
    _c("Compare Graham scan vs Jarvis march for convex hull", "MEDIUM", "comparison", "en"),
    # ── Adversarial: system design that is actually MEDIUM (single component) ──
    _c("Design a single-component rate limiter using a token bucket", "MEDIUM", "simple-code", "en"),
    _c("Design a cache eviction policy for a single in-memory cache", "MEDIUM", "simple-code", "en"),
    _c("Design a single retry mechanism with exponential backoff", "MEDIUM", "simple-code", "en"),
    _c("Design a simple circuit breaker for one service call", "MEDIUM", "simple-code", "en"),
    # ── Non-English MEDIUM ──
    _c("写一个递归下降解析器解析简单算术表达式", "MEDIUM", "simple-code", "zh"),
    _c("实现一个简单的词法分析器，识别标识符、数字和运算符", "MEDIUM", "simple-code", "zh"),
    _c("实现一个使用信号量的生产者-消费者", "MEDIUM", "simple-code", "zh"),
    _c("实现 B 树的插入操作", "MEDIUM", "simple-code", "zh"),
    _c("实现 Kruskal 算法求最小生成树", "MEDIUM", "simple-code", "zh"),
    _c("解释编译器如何将源代码转换为机器码", "MEDIUM", "explanation", "zh"),
    _c("解释虚拟内存如何通过页表工作", "MEDIUM", "explanation", "zh"),
    _c("比较 Raft 和 Paxos 的优缺点", "MEDIUM", "comparison", "zh"),
    _c("比较 B 树和 LSM 树在写密集场景下的表现", "MEDIUM", "comparison", "zh"),
    _c("簡単な算術式の再帰下降パーサーを書いてください", "MEDIUM", "simple-code", "ja"),
    _c("セマフォを使ったプロデューサー・コンシューマを実装してください", "MEDIUM", "simple-code", "ja"),
    _c("B木の挿入操作を実装してください", "MEDIUM", "simple-code", "ja"),
    _c("Kruskalのアルゴリズムで最小全域木を実装してください", "MEDIUM", "simple-code", "ja"),
    _c("コンパイラがソースコードを機械語に変換する仕組みを説明してください", "MEDIUM", "explanation", "ja"),
    _c("RaftとPaxosの比較をしてください", "MEDIUM", "comparison", "ja"),
    _c("간단한 산술 표현식용 재귀 하강 파서를 작성해주세요", "MEDIUM", "simple-code", "ko"),
    _c("세마포어를 사용한 생산자-소비자 구현해주세요", "MEDIUM", "simple-code", "ko"),
    _c("B-트리 삽입 연산을 구현해주세요", "MEDIUM", "simple-code", "ko"),
    _c("컴파일러가 소스 코드를 기계어로 변환하는 방식을 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("Raft와 Paxos 비교해주세요", "MEDIUM", "comparison", "ko"),
    _c("اكتب محلل نزول تكراري لتعبير حسابي بسيط", "MEDIUM", "simple-code", "ar"),
    _c("نفّذ منتج-مستهلك باستخدام الإشارات", "MEDIUM", "simple-code", "ar"),
    _c("اشرح كيف يحول المترجم الكود المصدري إلى كود آلي", "MEDIUM", "explanation", "ar"),
    _c("Напиши рекурсивный нисходящий парсер для простых арифметических выражений", "MEDIUM", "simple-code", "ru"),
    _c("Реализуй производитель-потребитель с семафорами", "MEDIUM", "simple-code", "ru"),
    _c("Объясни как компилятор преобразует исходный код в машинный", "MEDIUM", "explanation", "ru"),
    _c("Escribe un parser descendente recursivo para expresiones aritméticas simples", "MEDIUM", "simple-code", "es"),
    _c("Implementa productor-consumidor con semáforos", "MEDIUM", "simple-code", "es"),
    _c("Explica cómo el compilador transforma código fuente en código máquina", "MEDIUM", "explanation", "es"),
    _c("Schreibe einen rekursiven Abstiegsparser für einfache arithmetische Ausdrücke", "MEDIUM", "simple-code", "de"),
    _c("Implementiere Producer-Consumer mit Semaphoren", "MEDIUM", "simple-code", "de"),
    _c("Erkläre wie ein Compiler Quellcode in Maschinencode umwandelt", "MEDIUM", "explanation", "de"),
    _c("Écris un parser récursif descendant pour des expressions arithmétiques simples", "MEDIUM", "simple-code", "fr"),
    _c("Implémente producteur-consommateur avec des sémaphores", "MEDIUM", "simple-code", "fr"),
    _c("Explique comment le compilateur transforme le code source en code machine", "MEDIUM", "explanation", "fr"),
    _c("Escreva um parser descendente recursivo para expressões aritméticas simples", "MEDIUM", "simple-code", "pt"),
    _c("Implemente produtor-consumidor com semáforos", "MEDIUM", "simple-code", "pt"),
    _c("Explique como o compilador transforma código fonte em código de máquina", "MEDIUM", "explanation", "pt"),
    _c("सरल अंकगणितीय व्यंजक के लिए पुनरावर्ती अवरोही पार्सर लिखें", "MEDIUM", "simple-code", "hi"),
    _c("सेमाफोर का उपयोग करके उत्पादक-उपभोक्ता लागू करें", "MEDIUM", "simple-code", "hi"),
    _c("Basit aritmetik ifadeler için özyinelemeli inişli ayrıştırıcı yazın", "MEDIUM", "simple-code", "tr"),
    _c("Semafor kullanarak üretici-tüketici uygulayın", "MEDIUM", "simple-code", "tr"),
    _c("Viết parser đệ quy xuống cho biểu thức số học đơn giản", "MEDIUM", "simple-code", "vi"),
    _c("Triển khai producer-consumer bằng semaphore", "MEDIUM", "simple-code", "vi"),
    _c("Napisz parser rekurencyjny zstępujący dla prostych wyrażeń arytmetycznych", "MEDIUM", "simple-code", "pl"),
    _c("Zaimplementuj producent-konsument z semaforami", "MEDIUM", "simple-code", "pl"),
    # ── More MEDIUM to reach ~180 ──
    _c("Write unit tests for a B-tree insert function", "MEDIUM", "testing", "en"),
    _c("Debug this deadlock: two threads each hold one lock and wait for the other", "MEDIUM", "debugging", "en"),
    _c("Summarize the key differences between Raft and Paxos in 3 bullet points", "MEDIUM", "summary", "en"),
    _c("Review this TCP state machine implementation for edge cases", "MEDIUM", "code-review", "en"),
    _c("Extract all function names from this C source file", "MEDIUM", "extraction", "en"),
    _c("Convert this AST to three-address code", "MEDIUM", "structured-output", "en"),
    _c("Rewrite this scheduler to use a priority queue instead of a list", "MEDIUM", "rewrite", "en"),
    _c("Classify these network packets by protocol (TCP, UDP, ICMP)", "MEDIUM", "classification", "en"),
    _c("Write a script to profile cache hit rate for a given query workload", "MEDIUM", "simple-code", "en"),
    _c("Explain how the priority ceiling protocol prevents priority inversion", "MEDIUM", "explanation", "en"),
    _c("Compare Graham scan vs incremental algorithm for convex hull", "MEDIUM", "comparison", "en"),
    _c("Implement a simple Raft log replication (single node, no leader election)", "MEDIUM", "simple-code", "en"),
    _c("Write a function to serialize and deserialize a binary tree", "MEDIUM", "simple-code", "en"),
    _c("Explain how MVCC allows concurrent reads and writes", "MEDIUM", "explanation", "en"),
    _c("Design a single-component idempotency key store", "MEDIUM", "simple-code", "en"),
    _c("Create a script to visualize a control flow graph", "MEDIUM", "simple-code", "en"),
    _c("Summarize the steps of a typical compiler pipeline", "MEDIUM", "summary", "en"),
    _c("Review this graph algorithm for correctness and edge cases", "MEDIUM", "code-review", "en"),
    _c("Implement a simple applicative functor for optional values", "MEDIUM", "simple-code", "en"),
    _c("Explain how the Nyquist theorem limits sampling rate", "MEDIUM", "explanation", "en"),
    # ── More non-English MEDIUM to reach ~180 ──
    _c("实现一个简单的 LRU 页置换算法", "MEDIUM", "simple-code", "zh"),
    _c("写一个函数解析 IPv4 包头", "MEDIUM", "simple-code", "zh"),
    _c("实现 Tarjan 算法求强连通分量", "MEDIUM", "simple-code", "zh"),
    _c("解释 Raft 如何在故障下达成共识", "MEDIUM", "explanation", "zh"),
    _c("比较 LL(1) 和 LR 解析的适用场景", "MEDIUM", "comparison", "zh"),
    _c("B木のLRUページ置換を実装してください", "MEDIUM", "simple-code", "ja"),
    _c("IPv4パケットヘッダーを解析する関数を書いてください", "MEDIUM", "simple-code", "ja"),
    _c("Raftが障害下で合意に達する仕組みを説明してください", "MEDIUM", "explanation", "ja"),
    _c("LRU 페이지 교체 알고리즘을 구현해주세요", "MEDIUM", "simple-code", "ko"),
    _c("IPv4 패킷 헤더를 파싱하는 함수를 작성해주세요", "MEDIUM", "simple-code", "ko"),
    _c("Raft가 장애 상황에서 합의에 도달하는 방식을 설명해주세요", "MEDIUM", "explanation", "ko"),
    _c("اكتب دالة لتحليل رأس حزمة IPv4", "MEDIUM", "simple-code", "ar"),
    _c("اشرح كيف يحقق Raft الإجماع في وجود الأعطال", "MEDIUM", "explanation", "ar"),
    _c("Напиши функцию для разбора заголовка IPv4-пакета", "MEDIUM", "simple-code", "ru"),
    _c("Объясни как Raft достигает консенсуса при сбоях", "MEDIUM", "explanation", "ru"),
    _c("Escribe una función para parsear el encabezado de un paquete IPv4", "MEDIUM", "simple-code", "es"),
    _c("Explica cómo Raft logra consenso en presencia de fallos", "MEDIUM", "explanation", "es"),
    _c("Schreibe eine Funktion zum Parsen eines IPv4-Paketheaders", "MEDIUM", "simple-code", "de"),
    _c("Erkläre wie Raft bei Ausfällen Konsens erreicht", "MEDIUM", "explanation", "de"),
    _c("Écris une fonction pour parser l'en-tête d'un paquet IPv4", "MEDIUM", "simple-code", "fr"),
    _c("Explique comment Raft atteint le consensus en présence de pannes", "MEDIUM", "explanation", "fr"),
    _c("Escreva uma função para analisar o cabeçalho de um pacote IPv4", "MEDIUM", "simple-code", "pt"),
    _c("Explique como o Raft alcança consenso na presença de falhas", "MEDIUM", "explanation", "pt"),
    _c("IPv4 पैकेट हेडर पार्स करने के लिए फ़ंक्शन लिखें", "MEDIUM", "simple-code", "hi"),
    _c("IPv4 paket başlığını ayrıştıran bir fonksiyon yazın", "MEDIUM", "simple-code", "tr"),
    _c("Viết hàm phân tích tiêu đề gói IPv4", "MEDIUM", "simple-code", "vi"),
    _c("Napisz funkcję do parsowania nagłówka pakietu IPv4", "MEDIUM", "simple-code", "pl"),
    _c("实现 Graham 扫描算法计算凸包", "MEDIUM", "simple-code", "zh"),
    _c("Implemente o algoritmo de Graham para casca convexa", "MEDIUM", "simple-code", "pt"),
    _c("Implementuj algorytm Kruskala dla MST", "MEDIUM", "simple-code", "pl"),
    _c("グラハムスキャンで凸包を計算する関数を実装してください", "MEDIUM", "simple-code", "ja"),
    _c("그래함 스캔으로 볼록 껍질을 계산하는 함수를 구현해주세요", "MEDIUM", "simple-code", "ko"),
    _c("Implementuj Tarjanův algoritmus pro silně souvislé komponenty", "MEDIUM", "simple-code", "cs"),
]


# ═══════════════════════════════════════════════════════════
#  COMPLEX (~100)
# ═══════════════════════════════════════════════════════════

COMPLEX_B11: list[dict] = [
    # ── Compiler design multi-requirement ──
    _c(
        "Design a compiler frontend for a toy language with lexer, parser, AST, semantic analysis, and IR generation. Include error recovery and symbol table management.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a JIT compiler with bytecode interpretation, profiling, hot path detection, and native code generation. Include deoptimization support.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a multi-pass optimizer with constant propagation, dead code elimination, inlining, and register allocation. Include cost models for each pass.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a compiler backend targeting a custom ISA with instruction selection, scheduling, and register allocation. Include peephole optimization.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Operating systems multi-requirement ──
    _c(
        "Design a microkernel with process management, IPC, virtual memory, and device drivers. Include scheduling policies, paging, and capability-based security.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a userspace threading library with stack management, context switching, synchronization primitives, and integration with the system scheduler.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a file system with inodes, directory structure, journaling, and crash recovery. Include allocation strategies and caching.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a memory manager with buddy allocation, slab allocator, and page reclaim. Include OOM handling and cgroup integration.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Network protocols multi-requirement ──
    _c(
        "Design a TCP stack with congestion control, flow control, retransmission, and connection management. Include handling of out-of-order packets and duplicate ACKs.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build an HTTP/2 implementation with multiplexing, stream prioritization, header compression, and flow control. Include server push and connection migration.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a BGP implementation with route reflection, policy filtering, and multipath. Include convergence optimization and route dampening.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a QUIC stack with 0-RTT, connection migration, and multiplexing. Include TLS integration and loss detection.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Database internals multi-requirement ──
    _c(
        "Design a storage engine with WAL, buffer pool, B-tree indexes, and checkpointing. Include crash recovery, vacuum, and statistics collection.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a query executor with volcano model, join algorithms (nested loop, hash, merge), aggregation, and sort. Include cost-based plan selection.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a replication system with synchronous and asynchronous modes, failover, and conflict resolution. Include split-brain prevention.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement an LSM-based storage engine with leveled compaction, bloom filters, and range queries. Include write amplification optimization.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Distributed consensus multi-requirement ──
    _c(
        "Implement a Raft consensus module with leader election, log replication, membership changes, and snapshotting. Include handling of network partitions.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a distributed transaction coordinator with 2PC, 3PC fallback, and compensation. Include timeout handling and orphan resolution.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a replicated state machine with consensus, persistence, and linearizable reads. Include lease-based read optimization.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a multi-datacenter replication system with conflict resolution, causal consistency, and failover. Include topology awareness.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    # ── Real-time systems multi-requirement ──
    _c(
        "Design a real-time scheduler with EDF, rate monotonic, and mixed criticality support. Include admission control and overload handling.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build an automotive ECU software stack with AUTOSAR, CAN communication, diagnostic services, and OTA updates. Include safety monitoring.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a hard real-time system with WCET analysis, priority inheritance, and deterministic memory allocation. Include certification support.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a time-triggered architecture with slot-based scheduling, fault tolerance, and redundancy. Include clock synchronization.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Signal processing / robotics multi-requirement ──
    _c(
        "Design a real-time signal processing pipeline with FFT, filtering, feature extraction, and classification. Include latency bounds and buffering.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a robot motion planning system with inverse kinematics, collision detection, trajectory optimization, and real-time execution. Include joint limits.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a sensor fusion system with Kalman filter, EKF for non-linear dynamics, and multi-sensor integration. Include outlier rejection.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a computational geometry library with convex hull, Voronoi, Delaunay, and range queries. Include robustness for degenerate cases.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Graph algorithms multi-requirement ──
    _c(
        "Design a graph analytics platform with distributed storage, BFS/DFS/PageRank, and community detection. Include incremental updates.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a routing engine with shortest path, multi-criteria optimization, and dynamic updates. Include contraction hierarchies.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a flow network solver with max-flow, min-cut, and multi-commodity flow. Include capacity scaling and push-relabel.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a graph database with property graph model, Cypher-like query, and index support. Include transaction isolation.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Type theory / category theory multi-requirement ──
    _c(
        "Design a type checker for a language with Hindley-Milner, algebraic data types, and type classes. Include inference and error reporting.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a proof assistant kernel with dependent types, tactics, and term normalization. Include metaprogramming support.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a category-theoretic library with functors, monads, applicatives, and free monads. Include laws verification and documentation.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a bidirectional type checker with subtyping and gradual typing. Include blame tracking.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── Non-English COMPLEX ──
    _c(
        "设计一个编译器前端，包括词法分析、语法分析、AST、语义分析和 IR 生成。需要错误恢复和符号表管理。",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c(
        "设计一个 TCP 协议栈，包括拥塞控制、流量控制、重传和连接管理。需要处理乱序包和重复 ACK。",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c(
        "设计一个存储引擎，包括 WAL、缓冲池、B 树索引和检查点。需要崩溃恢复、vacuum 和统计收集。",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c(
        "实现一个 Raft 共识模块，包括领导者选举、日志复制、成员变更和快照。需要处理网络分区。",
        "COMPLEX",
        "complex-code",
        "zh",
    ),
    _c(
        "设计一个实时调度器，支持 EDF、速率单调和混合关键级。需要准入控制和过载处理。", "COMPLEX", "system-design", "zh"
    ),
    _c(
        "设计一个传感器融合系统，包括卡尔曼滤波、非线性 EKF 和多传感器集成。需要异常值剔除。",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c(
        "コンパイラフロントエンドを設計してください。レキサー、パーサー、AST、意味解析、IR生成を含め、エラー回復とシンボルテーブル管理を含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "TCPスタックを設計してください。輻輳制御、フロー制御、再送、接続管理を含め、順序不同パケットと重複ACKの処理を含めてください。",
        "COMPLEX",
        "system-design",
        "ja",
    ),
    _c(
        "Raftコンセンサスモジュールを実装してください。リーダー選出、ログ複製、メンバー変更、スナップショットを含め、ネットワーク分断の処理を含めてください。",
        "COMPLEX",
        "complex-code",
        "ja",
    ),
    _c(
        "컴파일러 프론트엔드를 설계하세요. 렉서, 파서, AST, 의미 분석, IR 생성, 오류 복구, 심볼 테이블 관리를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "TCP 스택을 설계하세요. 혼잡 제어, 흐름 제어, 재전송, 연결 관리, 순서 바뀐 패킷 및 중복 ACK 처리를 포함해야 합니다.",
        "COMPLEX",
        "system-design",
        "ko",
    ),
    _c(
        "Raft 합의 모듈을 구현하세요. 리더 선출, 로그 복제, 멤버십 변경, 스냅샷, 네트워크 분할 처리를 포함해야 합니다.",
        "COMPLEX",
        "complex-code",
        "ko",
    ),
    _c(
        "صمم واجهة مترجم تشمل المحلل المعجمي والنحوي وAST والتحليل الدلالي وتوليد IR. تضمن استعادة الأخطاء وإدارة جدول الرموز.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "صمم مكدس TCP مع التحكم في الازدحام والتدفق وإعادة الإرسال وإدارة الاتصال. تضمن معالجة الحزم غير المرتبة وACK المكررة.",
        "COMPLEX",
        "system-design",
        "ar",
    ),
    _c(
        "Спроектируй фронтенд компилятора: лексер, парсер, AST, семантический анализ, генерация IR. Включи восстановление после ошибок и таблицу символов.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Спроектируй стек TCP с управлением перегрузкой, потоком, повторной передачей и соединениями. Включи обработку неупорядоченных пакетов.",
        "COMPLEX",
        "system-design",
        "ru",
    ),
    _c(
        "Diseña un frontend de compilador con lexer, parser, AST, análisis semántico y generación de IR. Incluye recuperación de errores y tabla de símbolos.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    _c(
        "Diseña un stack TCP con control de congestión, flujo, retransmisión y gestión de conexiones. Incluye manejo de paquetes desordenados.",
        "COMPLEX",
        "system-design",
        "es",
    ),
    _c(
        "Entwerfe ein Compiler-Frontend mit Lexer, Parser, AST, semantischer Analyse und IR-Generierung. Inkl. Fehlerbehandlung und Symboltabelle.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    _c(
        "Entwerfe einen TCP-Stack mit Congestion Control, Flow Control, Retransmission und Verbindungsverwaltung. Inkl. Behandlung von Out-of-Order-Paketen.",
        "COMPLEX",
        "system-design",
        "de",
    ),
    _c(
        "Conçois un frontend de compilateur avec lexer, parser, AST, analyse sémantique et génération IR. Inclure récupération d'erreurs et table des symboles.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    _c(
        "Conçois une pile TCP avec contrôle de congestion, flux, retransmission et gestion des connexions. Inclure gestion des paquets désordonnés.",
        "COMPLEX",
        "system-design",
        "fr",
    ),
    _c(
        "Projete um frontend de compilador com lexer, parser, AST, análise semântica e geração de IR. Inclua recuperação de erros e tabela de símbolos.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "Projete uma pilha TCP com controle de congestionamento, fluxo, retransmissão e gerenciamento de conexões. Inclua tratamento de pacotes fora de ordem.",
        "COMPLEX",
        "system-design",
        "pt",
    ),
    _c(
        "कंपाइलर फ्रंटएंड डिज़ाइन करें: लेक्सर, पार्सर, AST, शब्दार्थ विश्लेषण, IR जनरेशन। त्रुटि पुनर्प्राप्ति और प्रतीक तालिका शामिल करें।",
        "COMPLEX",
        "system-design",
        "hi",
    ),
    _c(
        "Derleyici ön ucu tasarlayın: lexer, parser, AST, anlamsal analiz, IR üretimi. Hata kurtarma ve sembol tablosu yönetimi dahil edin.",
        "COMPLEX",
        "system-design",
        "tr",
    ),
    _c(
        "Thiết kế frontend trình biên dịch: lexer, parser, AST, phân tích ngữ nghĩa, sinh IR. Bao gồm khôi phục lỗi và quản lý bảng ký hiệu.",
        "COMPLEX",
        "system-design",
        "vi",
    ),
    _c(
        "Zaprojektuj frontend kompilatora: lekser, parser, AST, analiza semantyczna, generowanie IR. Uwzględnij odzyskiwanie błędów i tabelę symboli.",
        "COMPLEX",
        "system-design",
        "pl",
    ),
    # ── More COMPLEX to reach ~100 ──
    _c(
        "Design a type checker for a language with Hindley-Milner, algebraic data types, and type classes. Include inference, error reporting, and module system.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Build a distributed graph processing system with vertex-centric model, partitioning, and fault tolerance. Include checkpointing and recovery.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Design a real-time audio processing pipeline with sample rate conversion, filtering, and effects. Include latency optimization and buffer management.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a multi-version concurrency control system with snapshot isolation, conflict detection, and garbage collection of old versions.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a protocol buffer compiler with schema parsing, code generation for multiple languages, and plugin support. Include validation and documentation.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a distributed lock service with lease-based locking, fencing tokens, and failure detection. Include deadlock prevention.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a mesh network routing protocol with link-state, path selection, and failure recovery. Include congestion awareness.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Implement a garbage collector with generational collection, concurrent marking, and compaction. Include write barriers and root scanning.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    _c(
        "Design a continuous integration system for compilers with incremental builds, test parallelization, and regression detection. Include caching.",
        "COMPLEX",
        "system-design",
        "en",
    ),
    _c(
        "Build a formal verification tool for concurrent programs with model checking and symbolic execution. Include counterexample generation.",
        "COMPLEX",
        "complex-code",
        "en",
    ),
    # ── More non-English COMPLEX to reach ~100 ──
    _c(
        "设计一个查询执行器，包括火山模型、嵌套循环/哈希/归并连接、聚合和排序。需要基于代价的计划选择。",
        "COMPLEX",
        "complex-code",
        "zh",
    ),
    _c("实现一个 LSM 存储引擎，包括分层压缩、布隆过滤器和范围查询。需要优化写放大。", "COMPLEX", "complex-code", "zh"),
    _c(
        "设计一个图分析平台，包括分布式存储、BFS/DFS/PageRank 和社区发现。需要增量更新。",
        "COMPLEX",
        "system-design",
        "zh",
    ),
    _c(
        "クエリ実行エンジンを設計してください。ボルケーノモデル、ネステッドループ/ハッシュ/マージジョイン、集約、ソートを含め、コストベースのプラン選択を含めてください。",
        "COMPLEX",
        "complex-code",
        "ja",
    ),
    _c(
        "LSMストレージエンジンを実装してください。レベル圧縮、ブルームフィルター、範囲クエリを含め、書き込み増幅の最適化を含めてください。",
        "COMPLEX",
        "complex-code",
        "ja",
    ),
    _c(
        "쿼리 실행기를 설계하세요. 볼케이노 모델, 중첩 루프/해시/머지 조인, 집계, 정렬, 비용 기반 계획 선택을 포함해야 합니다.",
        "COMPLEX",
        "complex-code",
        "ko",
    ),
    _c(
        "LSM 스토리지 엔진을 구현하세요. 레벨 압축, 블룸 필터, 범위 쿼리, 쓰기 증폭 최적화를 포함해야 합니다.",
        "COMPLEX",
        "complex-code",
        "ko",
    ),
    _c(
        "صمم محرك تنفيذ استعلامات مع نموذج البركان، حلقات متداخلة/هاش/دمج، تجميع وفرز. تضمن اختيار خطة قائم على التكلفة.",
        "COMPLEX",
        "complex-code",
        "ar",
    ),
    _c(
        "Спроектируй исполнитель запросов с вулканической моделью, вложенными циклами/хэш/слиянием, агрегацией и сортировкой. Включи выбор плана по стоимости.",
        "COMPLEX",
        "complex-code",
        "ru",
    ),
    _c(
        "Diseña un ejecutor de consultas con modelo volcánico, joins anidados/hash/merge, agregación y ordenación. Incluye selección de plan basada en coste.",
        "COMPLEX",
        "complex-code",
        "es",
    ),
    _c(
        "Entwerfe einen Query-Executor mit Volcano-Modell, Nested-Loop/Hash/Merge-Joins, Aggregation und Sortierung. Inkl. kostenbasierte Planauswahl.",
        "COMPLEX",
        "complex-code",
        "de",
    ),
    _c(
        "Conçois un exécuteur de requêtes avec modèle volcanique, jointures nested-loop/hash/merge, agrégation et tri. Inclure sélection de plan par coût.",
        "COMPLEX",
        "complex-code",
        "fr",
    ),
    _c(
        "Projete um executor de consultas com modelo vulcânico, joins nested-loop/hash/merge, agregação e ordenação. Inclua seleção de plano baseada em custo.",
        "COMPLEX",
        "complex-code",
        "pt",
    ),
    _c(
        "क्वेरी एक्ज़ीक्यूटर डिज़ाइन करें: वोल्कैनो मॉडल, नेस्टेड लूप/हैश/मर्ज जॉइन, एग्रीगेशन, सॉर्ट। लागत-आधारित योजना चयन शामिल करें।",
        "COMPLEX",
        "complex-code",
        "hi",
    ),
    _c(
        "Sorgu yürütücüsü tasarlayın: volkan modeli, iç içe döngü/hash/merge join, agregasyon, sıralama. Maliyet tabanlı plan seçimi dahil edin.",
        "COMPLEX",
        "complex-code",
        "tr",
    ),
    _c(
        "Thiết kế trình thực thi truy vấn với mô hình volcano, nested-loop/hash/merge join, aggregation, sort. Bao gồm lựa chọn kế hoạch dựa trên chi phí.",
        "COMPLEX",
        "complex-code",
        "vi",
    ),
    _c(
        "Zaprojektuj wykonawcę zapytań z modelem wulkanowym, złączeniami nested-loop/hash/merge, agregacją i sortowaniem. Uwzględnij wybór planu oparty na koszcie.",
        "COMPLEX",
        "complex-code",
        "pl",
    ),
    _c(
        "Design a distributed tracing system with span propagation, sampling strategies, and storage backends. Include correlation IDs and service dependency graphs.",
        "COMPLEX",
        "system-design",
        "en",
    ),
]


# ═══════════════════════════════════════════════════════════
#  REASONING (~80)
# ═══════════════════════════════════════════════════════════

REASONING_B11: list[dict] = [
    # ── Formal proofs ──
    _c(
        "Prove that the set of regular languages is closed under intersection. Use the product construction.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the pumping lemma for regular languages holds. Show that if L is regular, then the lemma conditions are satisfied.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the set of context-free languages is closed under union but not under intersection.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that every NFA can be converted to an equivalent DFA. Give the subset construction and prove correctness.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the language {a^n b^n c^n | n >= 0} is not context-free using the pumping lemma for CFLs.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the rationals are dense in the reals. Use the definition of density.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove that a tree with n vertices has exactly n-1 edges. Use induction.", "REASONING", "formal-proof", "en"),
    _c(
        "Prove that every connected graph has a spanning tree. Construct it explicitly.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that the maximum flow value equals the minimum cut capacity. Use the max-flow min-cut theorem.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that a graph is bipartite if and only if it has no odd-length cycles. Show both directions.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    # ── Algorithm correctness proofs ──
    _c(
        "Prove that Dijkstra's algorithm correctly computes shortest paths when all edge weights are non-negative. Use loop invariants.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that Kruskal's algorithm produces a minimum spanning tree. Use the cut property.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the greedy activity selection algorithm yields an optimal solution. Use the exchange argument.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that Bellman-Ford correctly finds shortest paths when no negative cycles exist. Use induction on path length.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the Ford-Fulkerson method finds a maximum flow when capacities are integers. Show that each augmentation increases flow by at least 1.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that binary search runs in O(log n) time and finds the element if present. Use the loop invariant.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the greedy Huffman algorithm produces an optimal prefix code. Use the lemma about optimal codes for sorted frequencies.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that merge sort is correct and runs in O(n log n). Use the recursion tree and master theorem.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the two-pointer technique correctly finds a pair with given sum in a sorted array. Show termination.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that Prim's algorithm produces a minimum spanning tree. Use the cut property.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    # ── Math derivations ──
    _c(
        "Derive the closed-form solution for T(n) = 2T(n/2) + n using the master theorem. Show each case.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the expected number of comparisons in randomized quicksort. Use linearity of expectation.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the optimal policy for a simple MDP using value iteration. Prove convergence.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the Cramer-Rao lower bound for an unbiased estimator. Use the Cauchy-Schwarz inequality.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the bias-variance decomposition for squared error loss. Show that E[(Y - f)^2] = Bias^2 + Var + Noise.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the formula for the sum of the first n squares: 1² + 2² + ... + n² = n(n+1)(2n+1)/6. Use induction.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the optimal stopping rule for the secretary problem. Prove that 1/e is the threshold.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the recurrence for the number of binary search trees with n nodes. Solve it to get Catalan numbers.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the Fisher information for the normal distribution. Use the definition I(θ) = E[(∂/∂θ log f(X;θ))²].",
        "REASONING",
        "math-derivation",
        "en",
    ),
    _c(
        "Derive the optimal k for k-means when the true number of clusters is known. Use the elbow method justification.",
        "REASONING",
        "math-derivation",
        "en",
    ),
    # ── Induction / contradiction ──
    _c("Prove by induction that the sum of the first n odd numbers equals n².", "REASONING", "formal-proof", "en"),
    _c("Prove by induction that 2^n > n² for all n >= 5.", "REASONING", "formal-proof", "en"),
    _c("Prove by contradiction that there are infinitely many primes.", "REASONING", "formal-proof", "en"),
    _c("Prove by contradiction that √2 is irrational.", "REASONING", "formal-proof", "en"),
    _c("Prove by induction that every integer n >= 2 has a prime factorization.", "REASONING", "formal-proof", "en"),
    _c(
        "Prove by contradiction that the halting problem is undecidable. Use diagonalization.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove by induction that a full binary tree with n internal nodes has n+1 leaves.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove by contradiction that there is no largest prime number.", "REASONING", "formal-proof", "en"),
    _c(
        "Prove by induction that F(n) * F(n+1) = F(1)² + F(2)² + ... + F(n)² for Fibonacci numbers.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c("Prove by contradiction that if a graph has no odd cycles, it is bipartite.", "REASONING", "formal-proof", "en"),
    # ── Adversarial: proofs that look like explanations (but are REASONING) ──
    _c(
        "Show that the greedy coin change algorithm is optimal for coin systems {1, 5, 10, 25}. Prove it.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Demonstrate that the perceptron algorithm converges when the data is linearly separable. Provide a proof.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Establish that the set of decidable languages is closed under complement. Give a formal proof.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Verify that the greedy set cover algorithm has approximation ratio H(n). Prove the bound.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    # ── Game theory / logic ──
    _c(
        "Prove that every finite two-player zero-sum game has a Nash equilibrium in mixed strategies. Use the minimax theorem.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "Prove that in the iterated prisoner's dilemma, tit-for-tat is a Nash equilibrium when the discount factor is high enough.",
        "REASONING",
        "game-theory",
        "en",
    ),
    _c(
        "Prove that (A → B) → ((B → C) → (A → C)) is a tautology using natural deduction.",
        "REASONING",
        "formal-logic",
        "en",
    ),
    _c(
        "Prove that resolution is refutation-complete for propositional logic. Show that any unsatisfiable formula has a resolution refutation.",
        "REASONING",
        "formal-logic",
        "en",
    ),
    _c(
        "Prove that 2-SAT can be solved in linear time by reduction to strongly connected components.",
        "REASONING",
        "formal-logic",
        "en",
    ),
    # ── Non-English REASONING ──
    _c("证明：正则语言在交运算下封闭。使用乘积构造。", "REASONING", "formal-proof", "zh"),
    _c("证明 Dijkstra 算法在边权非负时正确计算最短路径。使用循环不变量。", "REASONING", "algorithm-proof", "zh"),
    _c("用主定理推导 T(n)=2T(n/2)+n 的闭式解。展示每种情况。", "REASONING", "math-derivation", "zh"),
    _c("用数学归纳法证明前 n 个奇数的和等于 n²。", "REASONING", "formal-proof", "zh"),
    _c("用反证法证明 √2 是无理数。", "REASONING", "formal-proof", "zh"),
    _c(
        "正規言語が交叉の下で閉じていることを証明してください。積構成を用いてください。",
        "REASONING",
        "formal-proof",
        "ja",
    ),
    _c(
        "Dijkstraのアルゴリズムが非負の重みで最短経路を正しく計算することを証明してください。ループ不変式を用いてください。",
        "REASONING",
        "algorithm-proof",
        "ja",
    ),
    _c(
        "マスター定理を用いてT(n)=2T(n/2)+nの閉形式を導出してください。各ケースを示してください。",
        "REASONING",
        "math-derivation",
        "ja",
    ),
    _c("数学的帰納法で、最初のn個の奇数の和がn²に等しいことを証明してください。", "REASONING", "formal-proof", "ja"),
    _c("정규 언어가 교집합에 대해 닫혀 있음을 증명하세요. 곱 구성을 사용하세요.", "REASONING", "formal-proof", "ko"),
    _c(
        "Dijkstra 알고리즘이 음이 아닌 가중치에서 최단 경로를 올바르게 계산함을 증명하세요. 루프 불변식을 사용하세요.",
        "REASONING",
        "algorithm-proof",
        "ko",
    ),
    _c(
        "마스터 정리를 사용해 T(n)=2T(n/2)+n의 닫힌 형태를 유도하세요. 각 경우를 보여주세요.",
        "REASONING",
        "math-derivation",
        "ko",
    ),
    _c("수학적 귀납법으로 처음 n개의 홀수의 합이 n²임을 증명하세요.", "REASONING", "formal-proof", "ko"),
    _c("أثبت أن اللغات المنتظمة مغلقة تحت التقاطع. استخدم البناء الضربي.", "REASONING", "formal-proof", "ar"),
    _c(
        "أثبت أن خوارزمية Dijkstra تحسب المسارات الأقصر بشكل صحيح عندما تكون الأوزان غير سالبة. استخدم ثوابت الحلقة.",
        "REASONING",
        "algorithm-proof",
        "ar",
    ),
    _c(
        "Докажи, что регулярные языки замкнуты относительно пересечения. Используй произведение автоматов.",
        "REASONING",
        "formal-proof",
        "ru",
    ),
    _c(
        "Докажи, что алгоритм Дейкстры правильно вычисляет кратчайшие пути при неотрицательных весах. Используй инвариант цикла.",
        "REASONING",
        "algorithm-proof",
        "ru",
    ),
    _c(
        "Demuestra que los lenguajes regulares son cerrados bajo intersección. Usa la construcción del producto.",
        "REASONING",
        "formal-proof",
        "es",
    ),
    _c(
        "Demuestra que el algoritmo de Dijkstra calcula correctamente los caminos más cortos con pesos no negativos. Usa invariantes de bucle.",
        "REASONING",
        "algorithm-proof",
        "es",
    ),
    _c(
        "Beweise, dass reguläre Sprachen unter Schnitt abgeschlossen sind. Verwende die Produktkonstruktion.",
        "REASONING",
        "formal-proof",
        "de",
    ),
    _c(
        "Beweise, dass Dijkstras Algorithmus bei nichtnegativen Gewichten korrekt kürzeste Wege berechnet. Verwende Schleifeninvarianten.",
        "REASONING",
        "algorithm-proof",
        "de",
    ),
    _c(
        "Démontre que les langages réguliers sont clos par intersection. Utilise la construction produit.",
        "REASONING",
        "formal-proof",
        "fr",
    ),
    _c(
        "Démontre que l'algorithme de Dijkstra calcule correctement les plus courts chemins avec des poids non négatifs. Utilise les invariants de boucle.",
        "REASONING",
        "algorithm-proof",
        "fr",
    ),
    _c(
        "Prove que as linguagens regulares são fechadas sob interseção. Use a construção do produto.",
        "REASONING",
        "formal-proof",
        "pt",
    ),
    _c(
        "Prove que o algoritmo de Dijkstra calcula corretamente os caminhos mais curtos com pesos não negativos. Use invariantes de loop.",
        "REASONING",
        "algorithm-proof",
        "pt",
    ),
    _c("सिद्ध करें कि नियमित भाषाएँ प्रतिच्छेदन के अंतर्गत संवृत हैं। गुणन निर्माण का उपयोग करें।", "REASONING", "formal-proof", "hi"),
    _c(
        "Düzenli dillerin kesişim altında kapalı olduğunu kanıtlayın. Çarpım yapısını kullanın.",
        "REASONING",
        "formal-proof",
        "tr",
    ),
    _c(
        "Chứng minh rằng các ngôn ngữ chính quy đóng dưới phép giao. Sử dụng cấu trúc tích.",
        "REASONING",
        "formal-proof",
        "vi",
    ),
    _c(
        "Udowodnij, że języki regularne są zamknięte ze względu na przecięcie. Użyj konstrukcji iloczynu.",
        "REASONING",
        "formal-proof",
        "pl",
    ),
    # ── More REASONING to reach ~80 ──
    _c(
        "Prove that the greedy interval scheduling algorithm is optimal. Use the exchange argument.",
        "REASONING",
        "algorithm-proof",
        "en",
    ),
    _c(
        "Prove that the set of recursively enumerable languages is closed under union. Give a constructive proof.",
        "REASONING",
        "formal-proof",
        "en",
    ),
    _c(
        "Prove that a graph has an Eulerian circuit if and only if every vertex has even degree. Show both directions.",
        "REASONING",
        "formal-proof",
        "en",
    ),
]


ALL_B11 = SIMPLE_B11 + MEDIUM_B11 + COMPLEX_B11 + REASONING_B11


def export(path=None):
    from pathlib import Path
    import json

    out = Path(path) if path else Path(__file__).parent.parent / "data" / "handcrafted_b11.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for case in ALL_B11:
            json.dump(case, f, ensure_ascii=False)
            f.write("\n")
    from collections import Counter

    tiers = Counter(c["expected_tier"] for c in ALL_B11)
    langs = Counter(c["lang"] for c in ALL_B11)
    print(f"Batch 11: {len(ALL_B11)} cases")
    print(f"  Tiers: {dict(tiers)}")
    print(f"  Languages: {len(langs)} — {dict(langs)}")


if __name__ == "__main__":
    import sys

    export(sys.argv[1] if len(sys.argv) > 1 else None)
