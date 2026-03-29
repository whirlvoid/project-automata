<script setup lang="ts">
import { commands } from "@/commands";

defineProps<{ isTextMod: boolean; isLoading: boolean; lineInput: string }>();
</script>
<template>
    <div v-if="isLoading" class="loader"></div>
    <div v-if="!isLoading">
        <span v-if="isTextMod">> </span>
        <span v-if="!isTextMod"><span class="system-name">automata</span>:~$ </span>
        <span>
            <span v-for="(cmdWord, wordIdx) in lineInput.split(/(\s+)/)" :key="wordIdx">
                <span :class="{ command: commands.hasOwnProperty(cmdWord), arg: cmdWord.startsWith(`-`) }">{{
                    cmdWord
                }}</span>
            </span>
        </span>
        <span class="cursor">I</span>
    </div>
</template>
<style scoped>
.system-name {
    color: #3f4880;
}
.command {
    color: #4b8c92;
}
.arg {
    color: #67615c;
}
.cursor {
    background-color: #4b8c92;
    color: #4b8c92;
    border-radius: 1.5px;
    margin-left: 2px;
    transition: background-color 0.1s;
    animation: blink 1s step-start infinite;
}
@keyframes blink {
    0%,
    50% {
        opacity: 1;
    }
    51%,
    100% {
        opacity: 0;
    }
}
.loader {
    /* background-color: #4b8c92; */
    color: #4b8c92;
    width: fit-content;
    clip-path: inset(0 100% 0 0);
    animation: l5 1s steps(4) infinite;
}
.loader:before {
    content: "...";
}
@keyframes l5 {
    to {
        clip-path: inset(0 -1ch 0 0);
    }
}
</style>
