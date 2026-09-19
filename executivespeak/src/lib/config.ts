export function isDemoMode(): boolean {
  if (process.env.DEMO_MODE === "true") return true;
  if (process.env.DEMO_MODE === "false") return false;
  return !process.env.DATABASE_URL || process.env.AI_PROVIDER === "mock";
}

export function getAppConfig() {
  return {
    demoMode: isDemoMode(),
    aiProvider: process.env.AI_PROVIDER ?? "mock",
    sttProvider: process.env.SPEECH_TO_TEXT_PROVIDER ?? "browser",
    ttsProvider: process.env.TEXT_TO_SPEECH_PROVIDER ?? "browser",
    pronunciationProvider: process.env.PRONUNCIATION_PROVIDER ?? "mock",
  };
}
