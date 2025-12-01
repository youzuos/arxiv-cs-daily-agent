"""Generate mock arXiv CS Daily data for frontend consumption."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
import random

# Categories for variety
CATEGORIES = [
    ["cs.AI", "cs.LG"],
    ["cs.CV", "cs.CL"],
    ["cs.AR", "cs.LG"],
    ["cs.CL", "cs.LG"],
    ["cs.LG", "cs.CR"],
    ["cs.CV", "cs.RO"],
    ["cs.LG", "cs.AI"],
    ["cs.CL"],
    ["cs.CV", "cs.AR"],
    ["cs.AI", "cs.HC"],
    ["cs.AR", "cs.LG"],
    ["cs.CV", "cs.LG"],
    ["cs.CL", "cs.LG"],
    ["cs.AI", "cs.DC"],
    ["cs.CL", "cs.LG"],
]

# Sample author names
AUTHOR_POOL = [
    ["Alice Zhang", "Ben Carter", "Chloe Davis"],
    ["David Lee", "Emma Wilson", "Frank Miller", "Grace Brown"],
    ["Henry Taylor", "Ivy Chen", "Jack Robinson"],
    ["Karen White", "Leo Garcia", "Mia Johnson", "Nathan Kim"],
    ["Olivia Park", "Paul Singh", "Quinn Adams"],
    ["Rachel Green", "Sam Patel", "Tina Wong", "Uma Rao"],
    ["Victor Chen", "Wendy Li", "Xavier Wang"],
    ["Yara Hassan", "Zoe Martinez", "Adam Klein"],
    ["Bella Scott", "Carlos Ruiz", "Diana Lee", "Ethan Moore"],
    ["Fiona Zhang", "George Harris", "Hannah Kim"],
    ["Ian Thompson", "Julia Adams", "Kevin Brown", "Lily Chen"],
    ["Michael Wong", "Nina Patel", "Oscar Garcia"],
    ["Paula Rodriguez", "Quincy Jones", "Rita Singh"],
    ["Sarah Johnson", "Tom Wilson", "Uma Patel", "Vincent Lee"],
    ["William Chen", "Yvonne Martin", "Zachary Brown"],
]

# Paper titles
TITLES = [
    "Efficient Neural Architecture Search via Multi-Objective Optimization",
    "Cross-Modal Retrieval with Vision-Language Transformers",
    "Hardware-Aware Pruning for Efficient Edge Deployment",
    "Multimodal Sentiment Analysis Using Graph Neural Networks",
    "Federated Learning with Differential Privacy Guarantees",
    "Real-Time Object Detection for Autonomous Vehicles",
    "Quantum-Inspired Optimization for Machine Learning",
    "Neural Machine Translation with Few-Shot Adaptation",
    "Energy-Efficient Computer Vision on Mobile Devices",
    "Self-Supervised Learning for Medical Image Analysis",
    "Robust Natural Language Understanding with Adversarial Training",
    "Hardware Acceleration for Graph Neural Networks",
    "Multi-Agent Reinforcement Learning for Resource Allocation",
    "Explainable AI for Clinical Decision Support",
    "Efficient Transformers for Long Document Processing",
]

# Abstracts
ABSTRACTS = [
    "This paper introduces a novel neural architecture search framework that balances model accuracy and computational efficiency. Our method achieves state-of-the-art results on multiple benchmark datasets while reducing search time by 40%.",
    "We propose a transformer-based approach for cross-modal retrieval between images and text. The model demonstrates significant improvements in retrieval accuracy across three standard benchmarks compared to previous methods.",
    "This work presents a hardware-aware pruning technique that optimizes neural networks for edge devices. Experimental results show 3x speedup on mobile CPUs without sacrificing accuracy.",
    "We develop a graph neural network framework for multimodal sentiment analysis that integrates text, audio, and visual features. Our approach outperforms existing methods on two challenging sentiment analysis datasets.",
    "This paper introduces a federated learning framework with rigorous differential privacy guarantees. We demonstrate practical privacy-utility tradeoffs across multiple distributed learning scenarios.",
    "We present a real-time object detection system optimized for autonomous vehicle applications. The method achieves 95% accuracy while maintaining 30 FPS on embedded hardware.",
    "This research explores quantum-inspired optimization algorithms for training deep neural networks. Our approach shows faster convergence and better generalization compared to classical optimizers.",
    "We propose a few-shot adaptation method for neural machine translation that requires minimal target language data. The approach achieves competitive performance across 10 language pairs with only 100 examples.",
    "This work introduces energy-efficient computer vision algorithms specifically designed for mobile devices. Our methods reduce energy consumption by 60% while maintaining competitive accuracy on vision tasks.",
    "We develop a self-supervised learning framework for medical image analysis that reduces annotation requirements. The method achieves state-of-the-art performance on three medical imaging datasets.",
    "This paper presents an adversarial training approach for robust natural language understanding. Our method improves model robustness against various textual attacks while maintaining performance on clean data.",
    "We design a specialized hardware accelerator for graph neural networks that achieves 5x speedup over GPU implementations. The architecture efficiently handles irregular graph structures common in real-world applications.",
    "This research explores multi-agent reinforcement learning for dynamic resource allocation in cloud computing environments. Our approach improves resource utilization by 25% compared to traditional schedulers.",
    "We develop an explainable AI system for clinical decision support that provides interpretable predictions. The framework helps clinicians understand model reasoning while maintaining high diagnostic accuracy.",
    "This paper introduces an efficient transformer architecture for processing long documents. Our method reduces memory requirements by 70% while maintaining performance on document understanding tasks.",
]


def generate_papers() -> list[dict]:
    """Generate 15 papers with 2025 dates."""
    papers = []
    base_date = datetime.now()  # Use current date
    
    for i in range(15):
        # Generate dates from recent weeks (last 2-3 months)
        # Ensure at least one paper is from today
        if i == 0:
            days_ago = 0  # First paper is always today
        else:
            days_ago = random.randint(0, 90)  # Random date within last 90 days
        paper_date = base_date - timedelta(days=days_ago)
        
        # Generate ID: 2501.XXXXX format (2025 papers)
        month = paper_date.month
        paper_id = f"25{month:02d}.{10000 + i:05d}"
        
        papers.append({
            "id": paper_id,
            "title": TITLES[i],
            "authors": AUTHOR_POOL[i],
            "submittedAt": paper_date.strftime("%Y-%m-%d"),
            "abstract": ABSTRACTS[i],
            "categories": CATEGORIES[i],
            "pdfUrl": f"https://arxiv.org/pdf/{paper_id}.pdf",
        })
    
    return papers


def main() -> None:
    target = Path("frontend/src/data")
    target.mkdir(parents=True, exist_ok=True)
    out_file = target / "papers.json"
    
    papers = generate_papers()
    out_file.write_text(json.dumps(papers, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {len(papers)} papers with 2025 dates to {out_file}")
    print(f"   Date range: {min(p['submittedAt'] for p in papers)} to {max(p['submittedAt'] for p in papers)}")


if __name__ == "__main__":
    main()
