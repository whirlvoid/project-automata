import { EHisTypes } from "@/shared/enums";

export interface ICommands {
    help: string[];
    info: string[];
    clear: string[];
    main: string[];
    echo: string[];
    mcp: string[];
    rag: string[];
    [key: string]: string[];
}

export interface IHistoryItem {
    cmd: string;
    out: string[];
    type: EHisTypes;
}

export interface IMcpBody {
    user_prompt: string;
    max_steps?: number;
    model_name?: string;
}
