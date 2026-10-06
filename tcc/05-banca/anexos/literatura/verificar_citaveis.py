#!/usr/bin/env python3
"""Reproduz a checagem dos dados citáveis [C#] contra os textos completos.

Uso: python3 tcc/05-banca/anexos/literatura/verificar_citaveis.py
Para cada [C#] verificado, procura no texto completo (tcc/01-literatura/textos/<chave>.txt)
os padrões que sustentam a afirmação e imprime linha + trecho. O veredito (correto/impreciso)
foi atribuído por leitura humana do trecho; está registrado em VEREDITO.
"""
import re, pathlib
BASE = pathlib.Path(__file__).resolve().parents[3] / "01-literatura" / "textos"

CHECKS = [
 # chave, C#, padrões (todos devem ser encontrados), veredito
 ("jin2025agentmd","C1",[r"0\.877 vs\. 0\.409"],"correto"),
 ("jin2025agentmd","C2",[r"outperforms CoT with GPT-4 \(0\.546 vs\. 0\.409\)"],"correto"),
 ("jin2025agentmd","C3",[r"correct \(52\.3%\) or partially correct \(28\.5%\)"],"correto"),
 ("jin2025agentmd","C4",[r"HEART Score and Canadian C-Spine Rule",r"incorrect assumptions"],"correto"),
 ("jin2025agentmd","C5",[r"six criteria",r"8\.4% \(42/500\)",r"91\.6%"],"impreciso"),
 ("jin2025agentmd","C6",[r"reused the 350 manually validated sets of parameters",r"used GPT-4 to expand them into a clinical vignette"],"correto"),
 ("jin2025agentmd","C7",[r"more comprehensive evaluations are required before"],"correto"),
 ("khandekar2024medcalc","C1",[r"one-shot demonstration further increases its accuracy to 50\.91%"],"correto"),
 ("khandekar2024medcalc","C2",[r"33\.75"],"correto"),
 ("khandekar2024medcalc","C3",[r"Overall\s+23\.69%\s+30\.29%\s+37\.92%\s+48\.51%"],"correto"),
 ("khandekar2024medcalc","C4",[r"GPT-4\s+0\.35 \(57%\)"],"correto"),
 ("khandekar2024medcalc","C5",[r"drop is much more drastic as the parameter count increases"],"correto"),
 ("khandekar2024medcalc","C6",[r"necessary \(but not sufficient\) condition"],"correto"),
 ("zhu2025medagentboard","C1",[r"do not consistently outperform"],"correto"),
 ("zhu2025medagentboard","C2",[r"ColaCare.s 82\.91% AUROC versus DeepSeek-V3.s 76\.86%",r"85\.99",r"94\.28"],"correto"),
 ("zhu2025medagentboard","C3",[r"largely driven by the power of the underlying base LLM"],"correto"),
 ("zhu2025medagentboard","C4",[r"Exploring hybrid architectures"],"correto"),
 ("zhu2025medagentboard","C5",[r"fail to elicit genuine domain-specific knowledge"],"correto"),
 ("zhu2025medagentboard","C6",[r"frequent JSON parsing errors",r"getting stuck in loops"],"correto"),
 ("zhu2025medagentboard","C7",[r"Table 13: Estimated cost \(USD\) on the selected test set for Task 1",r"CoT-SC prompting strategy is the most expensive"],"impreciso"),
 ("wang2025colacare","C1",[r"SHAP strategy to obtain feature importance weights"],"correto"),
 ("wang2025colacare","C2",[r"w/o Expert Models\s+27\.73"],"correto"),
 ("wang2025colacare","C3",[r"54\.05±4\.88",r"53\.59±4\.52"],"correto"),
 ("wang2025colacare","C4",[r"4\.3 Multimodal Fusion Network"],"correto"),
 ("wang2025colacare","C5",[r"\$0\.013 USD per patient",r"# API Requests 8\.56"],"correto"),
 ("wang2025colacare","C6",[r"confidence estimation and continuous learning"],"correto"),
 ("cemri2025mast","C1",[r"41% to 86\.7% failure rate on 7"],"correto"),
 ("cemri2025mast","C2",[r"0\.88",r"14 unique modes, clustered into 3 categories"],"correto"),
 ("cemri2025mast","C3",[r"FM-3\.2, 8\.20%",r"FM-3\.3, 9\.10%"],"correto"),
 ("cemri2025mast","C4",[r"many existing verifiers perform only superficial checks"],"correto"),
 ("cemri2025mast","C5",[r"\+15\.6% improvement in task success"],"correto"),
 ("cemri2025mast","C6",[r"improvements in the base model capabilities will be insufficient"],"correto"),
 ("cemri2025mast","C7",[r"standardized communication protocol",r"symbolic validation"],"correto"),
 ("lee2025shapllm","C1",[r"overall fidelity of 0\.783",r"exact match accuracy was 0\.425"],"correto"),
 ("lee2025shapllm","C2",[r"SHAP Polarity Error3"],"correto"),
 ("lee2025shapllm","C3",[r"Fidelity \(scored as 1/0\.66/0\.33 for 3/2/1 correct features\)"],"correto"),
 ("lee2025shapllm","C4",[r"safety: 3\.45 vs\. 4\.79"],"correto"),
 ("lee2025shapllm","C5",[r"performs all calculations outside the LLM",r"monitoring layer that flags or blocks"],"correto"),
 ("lee2025shapllm","C6",[r"TN0\.35910\.20\.70"],"correto"),
 ("lee2025shapllm","C7",[r"lack of a direct baseline comparison against standard SHAP"],"correto"),
 ("roeschl2026pipeline","C1",[r"0\.78 vs\. 0\.32 vs\. 0\.39 vs\. 0\.31"],"correto"),
 ("roeschl2026pipeline","C2",[r"0\.0% to 15\.8% for five of six models"],"correto"),
 ("roeschl2026pipeline","C3",[r"knowledge conflict",r"assigned a point for .Hypertension. in the HAS-BLED"],"correto"),
 ("roeschl2026pipeline","C4",[r"expert-curated prompting performs better than retrieval-based"],"correto"),
 ("roeschl2026pipeline","C5",[r"treating physicians tended to underestimate patient risk"],"correto"),
 ("zhu2026agenticexpl","C1",[r"mean Jaccard 0\.171 versus 0\.077",r"92\.9% versus 78\.6%"],"correto"),
 ("zhu2026agenticexpl","C2",[r"0\.762 versus 0\.143"],"correto"),
 ("zhu2026agenticexpl","C3",[r"paired with attribution-based checks before use in high-stakes"],"correto"),
 ("zhu2026agenticexpl","C4",[r"llama3\.2:3b",r"received cleaned first-24-hour patient data and the model-predicted mortality probability"],"correto"),
 ("zhu2026agenticexpl","C5",[r"Only 14 generated cases overlapped"],"correto"),
 ("khan2024prevent","C1",[r"25 datasets \(N=3,281,919\)",r"3,330,085 participants from 21"],"correto"),
 ("khan2024prevent","C2",[r"0\.774 \(0\.743, 0\.788\)",r"0\.736 \(0\.710, 0\.755\)"],"correto"),
 ("khan2024prevent","C3",[r"0\.54 \[0\.47, 0\.61\] and 0\.50 \[0\.39, 0\.52\]",r"overestimation of risk by about 50%"],"correto"),
 ("khan2024prevent","C4",[r"BMI <30, per 5 kg/m2 \| \* \| \* \| \* \| \*"],"correto"),
 ("khan2024prevent","C5",[r"5\.4%, 3\.6%, and 2\.5%",r"9\.3%, 6\.0%, and 4\.7%"],"correto"),
 ("khan2024prevent","C6",[r"R2 ≥ 0\.99 for 10-year"],"correto"),
 ("khan2024prevent","C7",[r"sex-specific, race-free",r"competing risk of non-CVD death"],"correto"),
]

def main():
    tot = achados = 0
    from collections import Counter
    vered = Counter()
    for chave, c, pats, v in CHECKS:
        txt = (BASE / f"{chave}.txt").read_text(errors="ignore")
        ok = True
        for p in pats:
            m = re.search(p.replace(" ", r"\s+"), txt)
            if not m:
                ok = False; print(f"[NÃO ENCONTRADO] {chave} {c}: {p}"); continue
            ln = txt.count("\n", 0, m.start()) + 1
            trecho = txt[max(0, m.start()-60):m.end()+60].replace("\n", " ")
            print(f"{chave} {c} L{ln}: ...{trecho}...")
        tot += 1; achados += ok; vered[v] += 1
    print(f"\n{tot} [C#] checados; {achados} com todos os padrões encontrados; vereditos: {dict(vered)}")

if __name__ == "__main__":
    main()
