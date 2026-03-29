<script setup lang="ts">
import type { IHistoryItem } from "@/shared/interfaces";
import { EHisTypes } from "@/shared/enums";
import { commands } from "@/commands";

defineProps<{
    history: IHistoryItem[];
}>();
</script>

<template>
    <div v-for="(historyElem, i) in history" :key="i">
        <div v-if="historyElem.type === EHisTypes.HEAD" class="head-section">
            <div
                v-for="(outLine, lineIdx) in historyElem.out"
                :key="`head-${i}-${lineIdx}`"
                :style="{ animationDelay: lineIdx * 0.1 + 's' }"
                :class="{ head: outLine.startsWith(`#`) }"
                class="fade-in"
            >
                <span v-for="(outWord, wordIdx) in outLine.split(/(\s+)/)" :key="wordIdx">
                    <span :class="{ command: commands.hasOwnProperty(outWord) }">{{ outWord }}</span>
                </span>
            </div>
        </div>
        <div v-if="historyElem.type === EHisTypes.CMD">
            <div>
                <span class="system-name">automata</span>:~$
                <span v-for="(cmdWord, wordIdx) in historyElem.cmd.split(/(\s+)/)" :key="wordIdx">
                    <span :class="{ command: commands.hasOwnProperty(cmdWord), arg: cmdWord.startsWith(`-`) }">{{
                        cmdWord
                    }}</span>
                </span>
            </div>
            <div
                v-for="(outLine, cmdIdx) in historyElem.out"
                :key="`head-${i}-${cmdIdx}`"
                :class="{ head: outLine.startsWith(`#`) }"
            >
                <div class="asd">{{ outLine }}</div>
            </div>
        </div>
        <div v-if="historyElem.type === EHisTypes.ERROR">
            <div>
                <span class="system-name">automata</span>:~$
                <span v-for="(cmdWord, wordIdx) in historyElem.cmd.split(/(\s+)/)" :key="wordIdx">
                    <span :class="{ command: commands.hasOwnProperty(cmdWord), arg: cmdWord.startsWith(`-`) }">{{
                        cmdWord
                    }}</span>
                </span>
            </div>
            <div v-for="(outLine, errorIdx) in historyElem.out" :key="`head-${i}-${errorIdx}`">
                <div class="error">{{ outLine }}</div>
            </div>
        </div>
        <div v-if="historyElem.type === EHisTypes.TEXT">
            <div>> {{ historyElem.cmd }}</div>
            <div v-for="(outLine, textIdx) in historyElem.out" :key="`head-${i}-${textIdx}`">
                <div>{{ outLine }}</div>
            </div>
        </div>
        <div v-if="historyElem.type === EHisTypes.RESPONSE">
            <div v-for="(outLine, responseIdx) in historyElem.out" :key="`head-${i}-${responseIdx}`">
                <div>{{ outLine }}</div>
            </div>
        </div>
    </div>
</template>
<style scoped>
.head-section{
    display: none;
}
@media (min-width: 1050px){
    .head-section{
        display: block;
    }
}
.fade-in {
    animation: fadeIn 0.12s linear;
    opacity: 0;
    animation-fill-mode: forwards;
}
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(14px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
.head {
    color: #4b8c92;
}
.system-name {
    color: #3f4880;
}
.command {
    color: #4b8c92;
}
.arg {
    color: #67615c;
}
.error {
    color: #67615c;
}
</style>
