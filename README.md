# Sifting Truth From Spectacle!
### A Multimodal Hindi Dataset for Misinformation Detection with Emotional Cues and Sentiments

## Overview
This repository accompanies the paper **“Sifting Truth From Spectacle! A Multimodal Hindi Dataset for Misinformation Detection with Emotional Cues and Sentiments.”**  
It introduces a **multimodal Hindi misinformation dataset** consisting of **6,544 article–image pairs**, enriched with **sentiment and emotion annotations**.

Unlike existing English-centric or unimodal datasets, this resource integrates **text, images, and affective signals**, while carefully removing explicit veracity cues to avoid artefact-driven performance inflation.

This is the **first Hindi dataset** to jointly support **multimodal misinformation detection and affective analysis**.

---

## Dataset Highlights
- **Language**: Hindi  
- **Samples**: 6,544 article–image pairs  
- **Modalities**: Text, Image  
- **Annotations**:
  - Veracity label (Genuine / Misinformation)
  - Sentiment
  - Emotion
- **Debiased**: Explicit veracity cues removed
- **Tasks Supported**:
  - Text-only classification
  - Image-only classification
  - Multimodal fusion
  - Affective-aware misinformation detection

---

## Experiments
The repository includes implementations and baselines. Experiments demonstrate the effectiveness of **text–image fusion** and the complementary role of **affective features**.  
We additionally analyze **readability differences** between genuine and misleading Hindi news articles.

---

## Citation
```
@ARTICLE{11318635,
  author={Kumar, Raghvendra and Bansal, Pulkit and Singh, Raunak Kumar and Saha, Sriparna},
  journal={IEEE Transactions on Affective Computing},
  title={Sifting Truth From Spectacle! a Multimodal Hindi Dataset for Misinformation Detection With Emotional Cues and Sentiments},
  year={2025},
  pages={1--12},
  doi={10.1109/TAFFC.2025.3649246}
}
```
---

## License

This dataset is released for academic research only.
Commercial use is not permitted without prior permission.
