import type { AIProvider, PronunciationProvider, SpeechToTextProvider, TextToSpeechProvider } from "./types";
import { MockAIProvider } from "./ai/mock-ai-provider";
import { OpenAIProvider } from "./ai/openai-provider";
import { getAppConfig } from "@/lib/config";

export function getAIProvider(): AIProvider {
  const { aiProvider } = getAppConfig();
  if (aiProvider === "openai" && process.env.OPENAI_API_KEY) {
    return new OpenAIProvider();
  }
  return new MockAIProvider();
}

export function getSpeechToTextProvider(): SpeechToTextProvider {
  return {
    name: getAppConfig().sttProvider,
    isBrowserSupported: () => typeof window !== "undefined" && "webkitSpeechRecognition" in window,
  };
}

export function getTextToSpeechProvider(): TextToSpeechProvider {
  return {
    name: getAppConfig().ttsProvider,
    async speak(text: string, options?: { rate?: number }) {
      if (typeof window === "undefined" || !window.speechSynthesis) return;
      const u = new SpeechSynthesisUtterance(text);
      u.rate = options?.rate ?? 1;
      window.speechSynthesis.speak(u);
    },
  };
}

export function getPronunciationProvider(): PronunciationProvider {
  return {
    name: getAppConfig().pronunciationProvider,
    async analyzeWord(word, transcriptContext) {
      if (!transcriptContext.toLowerCase().includes(word.toLowerCase())) return null;
      return {
        word,
        issue: "Check word stress and vowel clarity.",
        ipa: undefined,
      };
    },
  };
}
