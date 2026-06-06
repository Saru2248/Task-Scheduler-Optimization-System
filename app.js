/**
 * ==========================================================================
 *  Task Scheduler Optimization Dashboard JavaScript Engine
 *  Algorithms & Custom Max-Heap Logic (from scratch)
 * ==========================================================================
 */

// --- 1. TASK MODEL CLASS ---
class Task {
    constructor(id, name, priority, deadline, execTime, profit) {
        this.id = Number(id);
        this.name = String(name);
        this.priority = Number(priority);
        this.deadline = Number(deadline);
        this.execTime = Number(execTime);
        this.profit = Number(profit);
        
        // Output values
        this.scheduled = false;
        this.startTime = null;
        this.finishTime = null;
    }
}

// --- 2. CUSTOM BINARY MAX-HEAP PRIORITY QUEUE ---
class MaxHeapPriorityQueue {
    constructor() {
        this.heap = [];
    }

    insert(task) {
        this.heap.push(task);
        this.bubbleUp(this.heap.length - 1);
    }

    extractMax() {
        if (this.heap.length === 0) return null;
        if (this.heap.length === 1) return this.heap.pop();
        
        const max = this.heap[0];
        this.heap[0] = this.heap.pop();
        this.bubbleDown(0);
        return max;
    }

    bubbleUp(index) {
        while (index > 0) {
            const parent = Math.floor((index - 1) / 2);
            if (this.heap[index].profit > this.heap[parent].profit) {
                this.swap(index, parent);
                index = parent;
            } else {
                break;
            }
        }
    }

    bubbleDown(index) {
        const length = this.heap.length;
        while (true) {
            let largest = index;
            const left = 2 * index + 1;
            const right = 2 * index + 2;

            if (left < length && this.heap[left].profit > this.heap[largest].profit) {
                largest = left;
            }
            if (right < length && this.heap[right].profit > this.heap[largest].profit) {
                largest = right;
            }

            if (largest !== index) {
                this.swap(index, largest);
                index = largest;
            } else {
                break;
            }
        }
    }

    swap(i, j) {
        const temp = this.heap[i];
        this.heap[i] = this.heap[j];
        this.heap[j] = temp;
    }

    buildHeap(taskList) {
        this.heap = taskList.map(t => new Task(t.id, t.name, t.priority, t.deadline, t.execTime, t.profit));
        const start = Math.floor((this.heap.length - 2) / 2);
        for (let i = start; i >= 0; i--) {
            this.bubbleDown(i);
        }
    }
}

// --- 3. SCHEDULING ALGORITHMS WITH STEP TRACING ---

// [A] Greedy Deadline Scheduler
function greedyDeadlineScheduler(tasks) {
    const trace = ["Sorting tasks descending by profit..."];
    const sorted = [...tasks].sort((a, b) => b.profit - a.profit);
    
    sorted.forEach(t => trace.push(`Task: ${t.name} (Profit: $${t.profit}, Deadline: slot ${t.deadline})`));
    
    const maxDeadline = Math.max(...tasks.map(t => t.deadline), 0);
    const slots = new Array(maxDeadline + 1).fill(null);
    const scheduled = [];
    const missed = [];

    trace.push(`\nInitializing time slots 1 to ${maxDeadline}...`);

    for (let task of sorted) {
        let placed = false;
        // Search latest slot possible
        const targetSlotLimit = Math.min(task.deadline, maxDeadline);
        for (let slot = targetSlotLimit; slot > 0; slot--) {
            if (slots[slot] === null) {
                slots[slot] = task;
                placed = true;
                trace.push(`[OK] Placed "${task.name}" into free slot ${slot}.`);
                break;
            }
        }
        if (!placed) {
            task.scheduled = false;
            missed.push(task);
            trace.push(`[MISS] No free slots available <= deadline ${task.deadline} for "${task.name}".`);
        }
    }

    // Build execution order sequentially
    let currentTime = 0;
    trace.push("\nBuilding sequential timeline chart execution start times:");
    for (let slot = 1; slot <= maxDeadline; slot++) {
        if (slots[slot] !== null) {
            const task = slots[slot];
            task.scheduled = true;
            task.startTime = currentTime;
            task.finishTime = currentTime + task.execTime;
            scheduled.push(task);
            trace.push(` - t=${currentTime} to t=${task.finishTime}: Executing "${task.name}"`);
            currentTime = task.finishTime;
        }
    }

    return { scheduled, missed, totalProfit: scheduled.reduce((sum, t) => sum + t.profit, 0), totalTime: currentTime, trace };
}

// [B] Heap-based Priority Queue Scheduler
function priorityQueueScheduler(tasks) {
    const trace = ["Building Binary Max-Heap from scratch..."];
    const pq = new MaxHeapPriorityQueue();
    pq.buildHeap(tasks);
    
    pq.heap.forEach((t, idx) => {
        trace.push(`Heap Slot ${idx}: ${t.name} (Profit: $${t.profit})`);
    });

    const scheduled = [];
    const missed = [];
    let currentTime = 0;

    trace.push("\nExtracting max-profit elements sequentially from Heap:");

    while (pq.heap.length > 0) {
        const task = pq.extractMax();
        const finish = currentTime + task.execTime;

        if (finish <= task.deadline) {
            task.scheduled = true;
            task.startTime = currentTime;
            task.finishTime = finish;
            scheduled.push(task);
            trace.push(`[OK] Extracted "${task.name}". fits at t=${currentTime} to t=${finish} (Deadline ${task.deadline}).`);
            currentTime = finish;
        } else {
            task.scheduled = false;
            missed.push(task);
            trace.push(`[MISS] Extracted "${task.name}". Would finish at t=${finish} which violates deadline ${task.deadline}.`);
        }
    }

    return { scheduled, missed, totalProfit: scheduled.reduce((sum, t) => sum + t.profit, 0), totalTime: currentTime, trace };
}

// [C] Earliest Deadline First (EDF)
function earliestDeadlineFirstScheduler(tasks) {
    const trace = ["Sorting tasks ascending by Deadline (EDF)..."];
    const sorted = [...tasks].sort((a, b) => a.deadline - b.deadline || b.profit - a.profit);
    
    sorted.forEach(t => trace.push(`Task: ${t.name} (Deadline: ${t.deadline}, Duration: ${t.execTime})`));

    const scheduled = [];
    const missed = [];
    let currentTime = 0;

    trace.push("\nProcessing jobs sequentially:");

    for (let task of sorted) {
        const finish = currentTime + task.execTime;
        if (finish <= task.deadline) {
            task.scheduled = true;
            task.startTime = currentTime;
            task.finishTime = finish;
            scheduled.push(task);
            trace.push(`[OK] scheduled "${task.name}" at t=${currentTime} to t=${finish} <= deadline ${task.deadline}.`);
            currentTime = finish;
        } else {
            task.scheduled = false;
            missed.push(task);
            trace.push(`[MISS] "${task.name}" requires duration ${task.execTime}. Would finish at t=${finish} > deadline ${task.deadline}.`);
        }
    }

    return { scheduled, missed, totalProfit: scheduled.reduce((sum, t) => sum + t.profit, 0), totalTime: currentTime, trace };
}

// [D] Shortest Job First (SJF)
function shortestJobFirstScheduler(tasks) {
    const trace = ["Sorting tasks ascending by Duration (SJF)..."];
    const sorted = [...tasks].sort((a, b) => a.execTime - b.execTime || b.profit - a.profit);
    
    sorted.forEach(t => trace.push(`Task: ${t.name} (Duration: ${t.execTime}, Deadline: ${t.deadline})`));

    const scheduled = [];
    const missed = [];
    let currentTime = 0;

    trace.push("\nProcessing jobs sequentially:");

    for (let task of sorted) {
        const finish = currentTime + task.execTime;
        if (finish <= task.deadline) {
            task.scheduled = true;
            task.startTime = currentTime;
            task.finishTime = finish;
            scheduled.push(task);
            trace.push(`[OK] scheduled Shortest Job "${task.name}" at t=${currentTime} to t=${finish}.`);
            currentTime = finish;
        } else {
            task.scheduled = false;
            missed.push(task);
            trace.push(`[MISS] "${task.name}" would finish at t=${finish} which violates deadline ${task.deadline}.`);
        }
    }

    return { scheduled, missed, totalProfit: scheduled.reduce((sum, t) => sum + t.profit, 0), totalTime: currentTime, trace };
}

// [E] Combined Score Multi-criteria Scheduler
function combinedScoreScheduler(tasks, wPriority, wDeadline, wProfit) {
    const trace = [`Sorting tasks by combined weights: wPriority=${wPriority}, wDeadline=${wDeadline}, wProfit=${wProfit}`];
    
    const maxPriority = Math.max(...tasks.map(t => t.priority), 1);
    const maxDeadline = Math.max(...tasks.map(t => t.deadline), 1);
    const maxProfit = Math.max(...tasks.map(t => t.profit), 1);

    const scoredTasks = tasks.map(t => {
        const normPriority = t.priority / maxPriority;
        const normUrgency = (maxDeadline - t.deadline + 1) / maxDeadline; // tighter deadline = higher score
        const normProfit = t.profit / maxProfit;
        
        const score = (wPriority * normPriority) + (wDeadline * normUrgency) + (wProfit * normProfit);
        return { task: t, score };
    });

    scoredTasks.sort((a, b) => b.score - a.score);
    scoredTasks.forEach(st => {
        trace.push(`Scored: ${st.task.name} -> score=${st.score.toFixed(3)}`);
    });

    const scheduled = [];
    const missed = [];
    let currentTime = 0;

    for (let st of scoredTasks) {
        const task = st.task;
        const finish = currentTime + task.execTime;
        if (finish <= task.deadline) {
            task.scheduled = true;
            task.startTime = currentTime;
            task.finishTime = finish;
            scheduled.push(task);
            trace.push(`[OK] scheduled scored task "${task.name}" (score: ${st.score.toFixed(2)}) at t=${currentTime} to t=${finish}`);
            currentTime = finish;
        } else {
            task.scheduled = false;
            missed.push(task);
            trace.push(`[MISS] scored task "${task.name}" failed deadline ${task.deadline} at t=${finish}`);
        }
    }

    return { scheduled, missed, totalProfit: scheduled.reduce((sum, t) => sum + t.profit, 0), totalTime: currentTime, trace };
}

// --- 4. APP STATE & DEFAULTS ---
const AppState = {
    tasks: [],
    presets: {
        default: [
            { id: 1, name: "Database Backup", priority: 9, deadline: 4, execTime: 1, profit: 90 },
            { id: 2, name: "User Auth Service", priority: 8, deadline: 3, execTime: 2, profit: 80 },
            { id: 3, name: "API Rate Limiter", priority: 7, deadline: 5, execTime: 1, profit: 70 },
            { id: 4, name: "Email Notification", priority: 5, deadline: 6, execTime: 2, profit: 50 },
            { id: 5, name: "Log Aggregation", priority: 4, deadline: 2, execTime: 1, profit: 40 },
            { id: 6, name: "Cache Warmup", priority: 6, deadline: 5, execTime: 2, profit: 60 },
            { id: 7, name: "Report Gen", priority: 3, deadline: 8, execTime: 3, profit: 30 },
            { id: 8, name: "Payment API", priority: 10, deadline: 2, execTime: 1, profit: 100 }
        ],
        advanced: [
            { id: 1, name: "Feature A Build", priority: 8, deadline: 5, execTime: 2, profit: 80 },
            { id: 2, name: "Feature B Build", priority: 6, deadline: 4, execTime: 1, profit: 60 },
            { id: 3, name: "Hotfix Critical", priority: 10, deadline: 2, execTime: 1, profit: 100 },
            { id: 4, name: "Unit Test Sweep", priority: 4, deadline: 6, execTime: 2, profit: 40 },
            { id: 5, name: "Security Audit", priority: 9, deadline: 5, execTime: 2, profit: 90 },
            { id: 6, name: "Performance Run", priority: 6, deadline: 7, execTime: 3, profit: 65 }
        ]
    }
};

// --- 5. DOM SELECTORS ---
const dom = {
    btnDefault: document.getElementById("btn-preset-default"),
    btnAdvanced: document.getElementById("btn-preset-adv"),
    btnClear: document.getElementById("btn-clear-tasks"),
    taskForm: document.getElementById("task-form"),
    tbodyTasks: document.getElementById("tasks-tbody"),
    algoSelect: document.getElementById("algo-select"),
    btnRun: document.getElementById("btn-run"),
    btnCompare: document.getElementById("btn-compare"),
    
    // Sliders & Badges
    sliderPriority: document.getElementById("input-priority"),
    badgePriority: document.getElementById("badge-priority"),
    sliderDeadline: document.getElementById("input-deadline"),
    badgeDeadline: document.getElementById("badge-deadline"),
    sliderExec: document.getElementById("input-exec"),
    badgeExec: document.getElementById("badge-exec"),
    sliderProfit: document.getElementById("input-profit"),
    badgeProfit: document.getElementById("badge-profit"),
    
    // CSV file import
    csvUpload: document.getElementById("csv-upload"),

    // Combined weights panel & sliders
    weightsPanel: document.getElementById("combined-weights-panel"),
    wPriority: document.getElementById("weight-priority"),
    wDeadline: document.getElementById("weight-deadline"),
    wProfit: document.getElementById("weight-profit"),
    lblWPriority: document.getElementById("lbl-w-priority"),
    lblWDeadline: document.getElementById("lbl-w-deadline"),
    lblWProfit: document.getElementById("lbl-w-profit"),

    // Trace list
    traceLogList: document.getElementById("trace-log-list"),

    // Alert
    alertBox: document.getElementById("validation-alert"),
    alertMsg: document.getElementById("validation-msg"),

    // KPIs
    kpiProfit: document.getElementById("kpi-profit"),
    kpiRate: document.getElementById("kpi-rate"),
    kpiScheduled: document.getElementById("kpi-scheduled"),
    kpiTime: document.getElementById("kpi-time"),

    // Lists & Gantt
    ganttChart: document.getElementById("gantt-chart"),
    listScheduled: document.getElementById("list-scheduled"),
    listMissed: document.getElementById("list-missed"),

    // Heap TAB
    heapTree: document.getElementById("heap-tree-root"),
    heapArrayList: document.getElementById("heap-array-list"),

    // Comparison TAB
    tbodyComparison: document.getElementById("comparison-tbody"),
    barChartProfit: document.getElementById("bar-chart-profit"),

    // Form fields
    fieldId: document.getElementById("input-id"),
    fieldName: document.getElementById("input-name")
};

// --- 6. EVENT BINDINGS ---
document.addEventListener("DOMContentLoaded", () => {
    // Tab switching logic
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            btn.classList.add("active");
            document.getElementById(btn.dataset.tab).classList.add("active");
        });
    });

    // Preset buttons
    dom.btnDefault.addEventListener("click", () => loadPreset("default"));
    dom.btnAdvanced.addEventListener("click", () => loadPreset("advanced"));
    dom.btnClear.addEventListener("click", clearAllTasks);

    // Form submit
    dom.taskForm.addEventListener("submit", handleFormSubmit);

    // Run schedulers
    dom.btnRun.addEventListener("click", runCurrentScheduler);
    dom.btnCompare.addEventListener("click", runGlobalComparison);

    // Dynamic Slider badge updates
    dom.sliderPriority.addEventListener("input", () => dom.badgePriority.innerText = dom.sliderPriority.value);
    dom.sliderDeadline.addEventListener("input", () => dom.badgeDeadline.innerText = dom.sliderDeadline.value);
    dom.sliderExec.addEventListener("input", () => dom.badgeExec.innerText = dom.sliderExec.value);
    dom.sliderProfit.addEventListener("input", () => dom.badgeProfit.innerText = dom.sliderProfit.value);

    // Combined scorer weights panel visibility and values
    dom.algoSelect.addEventListener("change", toggleWeightsPanel);
    dom.wPriority.addEventListener("input", () => { dom.lblWPriority.innerText = dom.wPriority.value; runCurrentScheduler(); });
    dom.wDeadline.addEventListener("input", () => { dom.lblWDeadline.innerText = dom.wDeadline.value; runCurrentScheduler(); });
    dom.wProfit.addEventListener("input", () => { dom.lblWProfit.innerText = dom.wProfit.value; runCurrentScheduler(); });

    // File Upload handling
    dom.csvUpload.addEventListener("change", handleCsvUpload);

    // Educational Accordions
    document.querySelectorAll(".faq-question").forEach(q => {
        q.addEventListener("click", () => {
            q.parentElement.classList.toggle("active");
        });
    });

    // Load Default Preset at start
    loadPreset("default");
    runCurrentScheduler();
    incrementFormId();
});

// --- 7. HANDLER METHODS ---

function toggleWeightsPanel() {
    if (dom.algoSelect.value === "combined") {
        dom.weightsPanel.classList.remove("hidden");
    } else {
        dom.weightsPanel.classList.add("hidden");
    }
    runCurrentScheduler();
}

function loadPreset(key) {
    AppState.tasks = AppState.presets[key].map(t => new Task(t.id, t.name, t.priority, t.deadline, t.execTime, t.profit));
    renderTasksTable();
    hideAlert();
    incrementFormId();
    runCurrentScheduler();
}

function clearAllTasks() {
    AppState.tasks = [];
    renderTasksTable();
    hideAlert();
    dom.fieldId.value = 1;
    runCurrentScheduler();
}

function renderTasksTable() {
    dom.tbodyTasks.innerHTML = "";
    AppState.tasks.forEach(t => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${t.id}</td>
            <td><strong>${t.name}</strong></td>
            <td>${t.priority}</td>
            <td>${t.deadline}</td>
            <td>${t.execTime}</td>
            <td>$${t.profit}</td>
            <td><button class="btn-row-del" onclick="deleteTask(${t.id})"><i class="fa-solid fa-circle-xmark"></i></button></td>
        `;
        dom.tbodyTasks.appendChild(tr);
    });
}

window.deleteTask = function(id) {
    AppState.tasks = AppState.tasks.filter(t => t.id !== id);
    renderTasksTable();
    incrementFormId();
    runCurrentScheduler();
};

function incrementFormId() {
    const maxId = AppState.tasks.reduce((max, t) => t.id > max ? t.id : max, 0);
    dom.fieldId.value = maxId + 1;
}

function handleFormSubmit(e) {
    e.preventDefault();
    hideAlert();

    const id = parseInt(dom.fieldId.value);
    const name = dom.fieldName.value.trim();
    const priority = parseInt(dom.sliderPriority.value);
    const deadline = parseInt(dom.sliderDeadline.value);
    const execTime = parseInt(dom.sliderExec.value);
    const profit = parseInt(dom.sliderProfit.value);

    // Validation
    if (AppState.tasks.some(t => t.id === id)) {
        showAlert("Duplicate ID detected. Task ID must be unique.");
        return;
    }
    if (execTime > deadline) {
        showAlert(`Task duration (${execTime}) cannot exceed deadline (${deadline}). It can never finish on time.`);
        return;
    }

    const newTask = new Task(id, name, priority, deadline, execTime, profit);
    AppState.tasks.push(newTask);
    
    renderTasksTable();
    dom.fieldName.value = "";
    incrementFormId();
    runCurrentScheduler();
}

function handleCsvUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(evt) {
        const text = evt.target.result;
        const lines = text.split("\n");
        const newTasks = [];
        let errors = [];

        // Skip header line
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;

            const cols = line.split(",");
            if (cols.length < 6) {
                errors.push(`Row ${i} has insufficient fields.`);
                continue;
            }

            const tid = parseInt(cols[0]);
            const name = cols[1].trim();
            const priority = parseInt(cols[2]);
            const deadline = parseInt(cols[3]);
            const execTime = parseInt(cols[4]);
            const profit = parseInt(cols[5]);

            if (isNaN(tid) || isNaN(priority) || isNaN(deadline) || isNaN(execTime) || isNaN(profit)) {
                errors.push(`Row ${i} contains non-numeric values.`);
                continue;
            }

            if (execTime > deadline) {
                errors.push(`Row ${i} duration (${execTime}) exceeds deadline (${deadline}).`);
                continue;
            }

            newTasks.push(new Task(tid, name, priority, deadline, execTime, profit));
        }

        if (errors.length > 0) {
            showAlert("CSV load failures:\n" + errors.slice(0, 3).join("\n"));
        } else {
            hideAlert();
        }

        if (newTasks.length > 0) {
            AppState.tasks = newTasks;
            renderTasksTable();
            incrementFormId();
            runCurrentScheduler();
        }
    };
    reader.readAsText(file);
}

function showAlert(msg) {
    dom.alertMsg.innerText = msg;
    dom.alertBox.classList.remove("hidden");
}

function hideAlert() {
    dom.alertBox.classList.add("hidden");
}

// --- 8. RUN AND PLOT TIMELINE & HEAP ---

function runCurrentScheduler() {
    if (AppState.tasks.length === 0) {
        dom.ganttChart.innerHTML = "<div class='gantt-time-lbl' style='text-align:center; padding:1rem;'>No tasks available. Add tasks or load preset.</div>";
        dom.kpiProfit.innerText = "$0";
        dom.kpiRate.innerText = "0%";
        dom.kpiScheduled.innerText = "0/0";
        dom.kpiTime.innerText = "0 slots";
        return;
    }

    const algo = dom.algoSelect.value;
    let result;

    const workingTasks = AppState.tasks.map(t => new Task(t.id, t.name, t.priority, t.deadline, t.execTime, t.profit));

    if (algo === "greedy") {
        result = greedyDeadlineScheduler(workingTasks);
    } else if (algo === "pq") {
        result = priorityQueueScheduler(workingTasks);
    } else if (algo === "edf") {
        result = earliestDeadlineFirstScheduler(workingTasks);
    } else if (algo === "sjf") {
        result = shortestJobFirstScheduler(workingTasks);
    } else if (algo === "combined") {
        const wp = parseFloat(dom.wPriority.value);
        const wd = parseFloat(dom.wDeadline.value);
        const wpr = parseFloat(dom.wProfit.value);
        result = combinedScoreScheduler(workingTasks, wp, wd, wpr);
    }

    plotGanttChart(result);
    plotHeapTree();
    plotStepTrace(result.trace);
    updateKpis(result, AppState.tasks.length);
}

function updateKpis(result, totalTasks) {
    dom.kpiProfit.innerText = `$${result.totalProfit}`;
    const rate = totalTasks > 0 ? Math.round((result.scheduled.length / totalTasks) * 100) : 0;
    dom.kpiRate.innerText = `${rate}%`;
    dom.kpiScheduled.innerText = `${result.scheduled.length}/${totalTasks}`;
    dom.kpiTime.innerText = `${result.totalTime} slots`;
}

function plotGanttChart(result) {
    dom.ganttChart.innerHTML = "";
    dom.listScheduled.innerHTML = "";
    dom.listMissed.innerHTML = "";

    if (result.scheduled.length === 0) {
        dom.ganttChart.innerHTML = "<div class='gantt-time-lbl' style='text-align:center; padding:1rem;'>No tasks scheduled.</div>";
        return;
    }

    // Sort timeline by start time
    const sorted = [...result.scheduled].sort((a, b) => a.startTime - b.startTime);

    const totalTime = result.totalTime || 1;
    sorted.forEach(t => {
        const row = document.createElement("div");
        row.className = "gantt-row";

        const widthPercent = (t.execTime / totalTime) * 82;
        const leftPercent = (t.startTime / totalTime) * 82;

        row.innerHTML = `
            <div class="gantt-time-scale" style="left: ${leftPercent}%">t=${t.startTime}</div>
            <div class="gantt-bar" style="margin-left: ${leftPercent}%; width: ${widthPercent}%;">
                ${t.name} (+$${t.profit})
            </div>
            <div class="gantt-time-lbl" style="left: calc(${leftPercent}% + ${widthPercent}% + 10px)">Finish: t=${t.finishTime}</div>
        `;
        dom.ganttChart.appendChild(row);

        const li = document.createElement("li");
        li.innerHTML = `
            <span><strong>${t.name}</strong> (ID: ${t.id})</span>
            <span>Slot: ${t.startTime} - ${t.finishTime} | Profit: <strong>+$${t.profit}</strong></span>
        `;
        dom.listScheduled.appendChild(li);
    });

    if (result.missed.length === 0) {
        dom.listMissed.innerHTML = "<li>None. All tasks scheduled successfully!</li>";
    } else {
        result.missed.forEach(t => {
            const li = document.createElement("li");
            li.innerHTML = `
                <span><strong>${t.name}</strong> (ID: ${t.id})</span>
                <span>Deadline: ${t.deadline} | Duration: ${t.execTime} | Loss: <strong style="color:var(--danger)">$${t.profit}</strong></span>
            `;
            dom.listMissed.appendChild(li);
        });
    }
}

// --- 9. RENDER HEAP VISUALIZER ---

function plotHeapTree() {
    dom.heapTree.innerHTML = "";
    dom.heapArrayList.innerHTML = "";

    if (AppState.tasks.length === 0) {
        dom.heapTree.innerHTML = "<div>Add tasks to populate the heap</div>";
        return;
    }

    const pq = new MaxHeapPriorityQueue();
    pq.buildHeap(AppState.tasks);

    if (pq.heap.length === 0) return;

    const treeLevels = [];
    let i = 0;
    let level = 0;

    while (i < pq.heap.length) {
        const nodesAtLevel = Math.pow(2, level);
        const levelNodes = [];
        
        for (let j = 0; j < nodesAtLevel; j++) {
            if (i >= pq.heap.length) break;
            levelNodes.push({ index: i, task: pq.heap[i] });
            i++;
        }
        
        treeLevels.push(levelNodes);
        level++;
    }

    treeLevels.forEach(lvl => {
        const lvlDiv = document.createElement("div");
        lvlDiv.className = "heap-level";
        
        lvl.forEach(nodeInfo => {
            const nodeDiv = document.createElement("div");
            nodeDiv.className = `heap-node`;
            nodeDiv.innerHTML = `
                <div class="node-name">${nodeInfo.task.name.substring(0, 7)}</div>
                <div class="node-val">$${nodeInfo.task.profit}</div>
            `;
            lvlDiv.appendChild(nodeDiv);

            const cell = document.createElement("div");
            cell.className = `heap-array-cell ${nodeInfo.index === 0 ? 'active-root' : ''}`;
            cell.innerHTML = `
                <strong>${nodeInfo.task.name.substring(0, 5)}</strong>
                <span>Idx: ${nodeInfo.index} (P: ${nodeInfo.task.profit})</span>
            `;
            dom.heapArrayList.appendChild(cell);
        });
        
        dom.heapTree.appendChild(lvlDiv);
    });
}

// --- 10. PLOT STEP-BY-STEP TRACE LOG ---

function plotStepTrace(trace) {
    dom.traceLogList.innerHTML = "";
    if (!trace) return;

    trace.forEach(line => {
        const div = document.createElement("div");
        div.className = "trace-item";
        
        if (line.startsWith("[OK]")) {
            div.className = "trace-item trace-ok";
        } else if (line.startsWith("[MISS]")) {
            div.className = "trace-item trace-miss";
        } else if (line.startsWith("Sorting") || line.startsWith("Extracting") || line.startsWith("Initializing")) {
            div.className = "trace-item trace-header";
        }
        
        div.innerText = line;
        dom.traceLogList.appendChild(div);
    });
}

// --- 11. MATRIX COMPARISONS & CHARTING ---

function runGlobalComparison() {
    if (AppState.tasks.length === 0) return;

    const tGreedy = AppState.tasks.map(t => new Task(t.id, t.name, t.priority, t.deadline, t.execTime, t.profit));
    const tPQ = AppState.tasks.map(t => new Task(t.id, t.name, t.priority, t.deadline, t.execTime, t.profit));
    const tEDF = AppState.tasks.map(t => new Task(t.id, t.name, t.priority, t.deadline, t.execTime, t.profit));
    const tSJF = AppState.tasks.map(t => new Task(t.id, t.name, t.priority, t.deadline, t.execTime, t.profit));
    const tComb = AppState.tasks.map(t => new Task(t.id, t.name, t.priority, t.deadline, t.execTime, t.profit));

    const wp = parseFloat(dom.wPriority.value);
    const wd = parseFloat(dom.wDeadline.value);
    const wpr = parseFloat(dom.wProfit.value);

    const results = {
        "Greedy Deadline": greedyDeadlineScheduler(tGreedy),
        "Priority Queue (Heap)": priorityQueueScheduler(tPQ),
        "Earliest Deadline First (EDF)": earliestDeadlineFirstScheduler(tEDF),
        "Shortest Job First (SJF)": shortestJobFirstScheduler(tSJF),
        "Combined Score": combinedScoreScheduler(tComb, wp, wd, wpr)
    };

    dom.tbodyComparison.innerHTML = "";
    dom.barChartProfit.innerHTML = "";

    const maxProfitVal = Math.max(...Object.values(results).map(r => r.totalProfit), 1);

    for (let [name, res] of Object.entries(results)) {
        const tr = document.createElement("tr");
        const rate = AppState.tasks.length > 0 ? Math.round((res.scheduled.length / AppState.tasks.length) * 100) : 0;
        
        tr.innerHTML = `
            <td><strong>${name}</strong></td>
            <td><span class="text-scheduled">${res.scheduled.length}</span></td>
            <td><span class="text-danger">${res.missed.length}</span></td>
            <td><strong class="text-success">$${res.totalProfit}</strong></td>
            <td><strong>${rate}%</strong></td>
            <td><span class="text-time">${res.totalTime} units</span></td>
        `;
        dom.tbodyComparison.appendChild(tr);

        const widthPercent = (res.totalProfit / maxProfitVal) * 100;
        const isBest = res.totalProfit === maxProfitVal;

        const chartRow = document.createElement("div");
        chartRow.className = "bar-chart-row";
        chartRow.innerHTML = `
            <div class="bar-label">${name}</div>
            <div class="bar-track">
                <div class="bar-fill ${isBest ? 'best-bar' : ''}" style="width: ${widthPercent}%"></div>
            </div>
            <div class="bar-val">$${res.totalProfit}</div>
        `;
        dom.barChartProfit.appendChild(chartRow);
    }

    document.querySelector("[data-tab='tab-comparison']").click();
}
