export interface PronunciationEntry {
  word: string;
  issue: string;
  ipa: string;
  slowTip: string;
}

export const PRONUNCIATION_WORD_BANK: PronunciationEntry[] = [
  {
    word: "architecture",
    issue: "Stress the second syllable: ar-KI-tec-ture (not ar-chi-TEK-ture)",
    ipa: "/ˈɑːrkɪtektʃər/",
    slowTip: "AR — ki — TEK — chur",
  },
  {
    word: "development",
    issue: "Reduce syllables naturally: di-VEL-up-ment",
    ipa: "/dɪˈveləpmənt/",
    slowTip: "di — VEL — up — ment",
  },
  {
    word: "specifically",
    issue: "Clear /sp/ cluster at start; stress second syllable",
    ipa: "/spəˈsɪfɪkli/",
    slowTip: "spuh — SIF — ih — klee",
  },
  {
    word: "recommend",
    issue: "Stress last syllable: rek-uh-MEND",
    ipa: "/ˌrekəˈmend/",
    slowTip: "rek — uh — MEND",
  },
  {
    word: "priority",
    issue: "Avoid 'prior-IT-ee' — use prahy-AWR-i-tee",
    ipa: "/praɪˈɔːrəti/",
    slowTip: "pry — OR — uh — tee",
  },
];

export function lookupPronunciation(word: string): PronunciationEntry | undefined {
  return PRONUNCIATION_WORD_BANK.find((w) => w.word.toLowerCase() === word.toLowerCase());
}

export function detectWordsInTranscript(transcript: string): PronunciationEntry[] {
  const lower = transcript.toLowerCase();
  return PRONUNCIATION_WORD_BANK.filter((e) => lower.includes(e.word));
}
