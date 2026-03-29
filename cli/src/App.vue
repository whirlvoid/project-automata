<script setup lang="ts">
import { ref, watch, nextTick } from "vue";
import asxios, { AxiosError } from "axios";
import type { IHistoryItem, IMcpBody } from "@/shared/interfaces";
import { EHisTypes, ECmd } from "@/shared/enums";
import { commands } from "@/commands";
import { head } from "@/head";
import History from "@/components/History.vue";
import TextLine from "@/components/TextLine.vue";

const history = ref<IHistoryItem[]>([{ cmd: "", out: head, type: EHisTypes.HEAD }]);
const commandHistory = ref<string[]>([]);
const commandHistoryIdx = ref(-1);
const lineInput = ref("");
const isTextMod = ref(false);
const isLoading = ref(false);
const isWaitingMCPPrompt = ref(false);
const isWaitingRAGPrompt = ref(false);
const mainRef = ref<HTMLElement | null>(null);
const inputRef = ref<HTMLElement | null>(null);

const checkMcpCmd = (cmdTrim: string) => {
    const parts: string[] = cmdTrim.split(/\s+/);
    if (parts[0] && parts[0] !== ECmd.MCP) {
        return false;
    }
    for (let i = 1; i < parts.length; i++) {
        const part = parts[i];
        if (!part?.startsWith("-m=") && !part?.startsWith("-ms=")) {
            return false;
        }
    }
    return true;
};

const run_default_command = (cmd: string) => {
    const cmdTrim: string = cmd.trim();
    if (cmdTrim === ECmd.CLEAR) {
        history.value = [];
        lineInput.value = "";
        return;
    }
    if (cmdTrim === ECmd.MAIN) {
        history.value = [];
        history.value.push({ cmd: "", out: head, type: EHisTypes.HEAD });
        lineInput.value = "";
        return;
    }
    if (cmdTrim.startsWith(`${ECmd.ECHO} `)) {
        const out_elem: string = cmd.substring(5);
        history.value.push({ cmd, out: [out_elem], type: EHisTypes.CMD });
        lineInput.value = "";
        return;
    }
    if (checkMcpCmd(cmdTrim)) {
        history.value.push({ cmd, out: [""], type: EHisTypes.CMD });
        lineInput.value = "";
        isWaitingMCPPrompt.value = true;
        isTextMod.value = true;
        return;
    }
    if (cmdTrim === ECmd.RAG) {
        history.value.push({ cmd, out: [""], type: EHisTypes.CMD });
        lineInput.value = "";
        isWaitingRAGPrompt.value = true;
        isTextMod.value = true;
        return;
    }
    if (commands[cmdTrim]) {
        const out: string[] = commands[cmdTrim];
        history.value.push({ cmd, out, type: EHisTypes.CMD });
        lineInput.value = "";
        return;
    }
    const error_message: string = `command not found: ${cmd}`;
    history.value.push({ cmd, out: [error_message], type: EHisTypes.ERROR });
    lineInput.value = "";
};

const parse_mcp_cmd = (lastCmd: string, body: IMcpBody) => {
    const lastCmdTrim: string = lastCmd.trim();
    const parts = lastCmdTrim.split(/\s+/);
    parts.forEach((part) => {
        if (part.startsWith("-ms=")) {
            body.max_steps = +part.substring(4);
        } else if (part.startsWith("-m=")) {
            body.model_name = part.substring(3);
        }
    });
    return body;
};

const run_agent = async (cmd: string) => {
    const lastCmd: string = history.value[history.value.length - 1]?.cmd || "";
    let body: IMcpBody = { user_prompt: cmd };
    body = parse_mcp_cmd(lastCmd, body);
    history.value.push({ cmd, out: [""], type: EHisTypes.TEXT });
    lineInput.value = "";
    let output: string;
    isLoading.value = true;
    try {
        const response = await asxios.post("http://localhost:8000/api/v1.0/execute", body);
        output = response.data.output;
    } catch (err: unknown) {
        if (err instanceof AxiosError) {
            output = err.response?.data?.detail || "Server error.";
        } else {
            output = "Server error.";
        }
    } finally {
        isLoading.value = false;
    }
    history.value.push({ cmd: "", out: [output], type: EHisTypes.RESPONSE });
    isTextMod.value = false;
    isWaitingMCPPrompt.value = false;
    return;
};

const run_rag = async (cmd: string) => {
    history.value.push({ cmd, out: [""], type: EHisTypes.TEXT });
    history.value.push({ cmd: "", out: ["Coming soon"], type: EHisTypes.RESPONSE });
    isTextMod.value = false;
    isWaitingRAGPrompt.value = false;
    return;
};

const run = async () => {
    if (!lineInput.value.trim()) {
        lineInput.value = "";
        focusInput();
        return;
    }
    const cmd: string = lineInput.value;
    if (cmd && commandHistory.value[commandHistory.value.length - 1] !== cmd) {
        commandHistory.value.push(cmd);
    }
    commandHistoryIdx.value = commandHistory.value.length;

    if (isWaitingMCPPrompt.value) {
        await run_agent(cmd);
        focusInput();
        return;
    }

    if (isWaitingRAGPrompt.value) {
        await run_rag(cmd);
        focusInput();
        return;
    }

    run_default_command(cmd);
    focusInput();
};

const handleKeydown = (e: KeyboardEvent) => {
    const forbiddenKeys = ["ArrowLeft", "ArrowRight"];
    if (forbiddenKeys.includes(e.key)) {
        e.preventDefault();
        return;
    }
    if (e.key === "ArrowUp") {
        e.preventDefault();
        if (commandHistory.value.length > 0 && commandHistoryIdx.value > 0) {
            commandHistoryIdx.value--;
            const cmd = commandHistory.value[commandHistoryIdx.value];
            if (cmd !== undefined) {
                lineInput.value = cmd;
            }
        }
    }
    if (e.key === "ArrowDown") {
        e.preventDefault();
        if (commandHistoryIdx.value < commandHistory.value.length - 1) {
            commandHistoryIdx.value++;
            const cmd = commandHistory.value[commandHistoryIdx.value];
            if (cmd !== undefined) {
                lineInput.value = cmd;
            }
        }
    }
};

watch(
    history,
    async () => {
        await nextTick();
        if (mainRef.value) {
            mainRef.value.scrollTop = mainRef.value.scrollHeight;
        }
    },
    { deep: true },
);

const focusInput = () => {
    inputRef.value?.focus();
};
</script>

<template>
    <div @click="focusInput" class="terminal">
        <div ref="mainRef" class="main">
            <History :history="history"></History>
            <TextLine :isTextMod="isTextMod" :isLoading="isLoading" :lineInput="lineInput"></TextLine>
        </div>
        <input
            ref="inputRef"
            type="text"
            v-model="lineInput"
            :disabled="isLoading"
            @keyup.enter="run"
            @keydown="handleKeydown"
            @blur="focusInput"
            class="hidden-input"
        />
    </div>
</template>

<style scoped>
@font-face {
    font-family: "Ioskeley Mono";
    src: url("./assets/fonts/IoskeleyMono-Regular.ttf") format("truetype");
    font-weight: normal;
    font-style: normal;
}
.terminal {
    background-color: #faf8f5;
    border: 1px solid #d9d9d0;
    border-radius: 20px;
    margin: 0;
    padding: 20px;
    min-height: calc(100dvh - 60px);
    cursor: text;
    font-size: 15px;
    font-family: "Ioskeley Mono", Courier, monospace;
}
.main {
    max-height: calc(100dvh - 60px);
    max-width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    white-space: pre-wrap;
    word-break: break-all;
    padding-right: 20px;
}
.main::-webkit-scrollbar {
    width: 10px;
}
.main::-webkit-scrollbar-track {
    background: #f5f2ee;
    border-radius: 2px;
}
.main::-webkit-scrollbar-thumb {
    background: #d9d9d0;
    border-radius: 2px;
}
.hidden-input {
    position: fixed;
    top: -100px;
    left: -100px;
    opacity: 0;
    pointer-events: none;
}
</style>
