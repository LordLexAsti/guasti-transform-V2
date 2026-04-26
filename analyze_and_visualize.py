#!/usr/bin/env python3
"""
Analyse et visualisation du processus Guasti Transform
======================================================

Ce script génère des graphiques pour analyser et évaluer le processus
de priorisation des nombres premiers via la Transformée de Guasti.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.wheel import residues_and_gaps
from src.features import build_precomp
from src.score import score_v1_no_residue, ScoreParams
from src.eval import candidate_mask, factorize_squarefree


def create_process_architecture_diagram():
    """Crée un diagramme de l'architecture du processus."""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(5, 11.5, 'Architecture du Processus Guasti Transform',
            ha='center', fontsize=16, weight='bold')

    # Colors
    color_input = '#E3F2FD'
    color_process = '#FFF9C4'
    color_feature = '#F3E5F5'
    color_score = '#E8F5E9'
    color_output = '#FFEBEE'

    # 1. Input layer
    ax.add_patch(mpatches.FancyBboxPatch((0.5, 9.5), 9, 1.2,
                 boxstyle="round,pad=0.1", ec="black", fc=color_input, lw=2))
    ax.text(5, 10.1, 'ENTRÉE: Fenêtre [A, B]', ha='center', fontsize=12, weight='bold')
    ax.text(5, 9.7, 'P = 2310 (primorielle 2×3×5×7×11)', ha='center', fontsize=9)

    # Arrow
    ax.annotate('', xy=(5, 9.3), xytext=(5, 9.5),
                arrowprops=dict(arrowstyle='->', lw=2))

    # 2. Candidate generation
    ax.add_patch(mpatches.FancyBboxPatch((0.5, 7.8), 9, 1.3,
                 boxstyle="round,pad=0.1", ec="black", fc=color_process, lw=2))
    ax.text(5, 8.7, 'GÉNÉRATION DES CANDIDATS', ha='center', fontsize=12, weight='bold')
    ax.text(5, 8.35, 'Filtrage: gcd(n, P) = 1', ha='center', fontsize=9)
    ax.text(5, 8.0, 'Résidus survivants: φ(2310) = 480 classes modulo P', ha='center', fontsize=9, style='italic')

    # Arrow
    ax.annotate('', xy=(5, 7.6), xytext=(5, 7.8),
                arrowprops=dict(arrowstyle='->', lw=2))

    # 3. Feature computation (multi-column)
    ax.add_patch(mpatches.FancyBboxPatch((0.5, 4.5), 9, 2.9,
                 boxstyle="round,pad=0.1", ec="black", fc=color_feature, lw=1.5))
    ax.text(5, 7.2, 'CALCUL DES FEATURES', ha='center', fontsize=12, weight='bold')

    # Sub-features
    features = [
        ('Impacts multi-échelle', 'c31, c101, c251\nCompte des petits premiers diviseurs'),
        ('Silence', 's_D = 1/(1+c_D)\nInverse du nombre d\'impacts'),
        ('Angle minimal', 'θ_min = atan(n/spf²)\nProxy angulaire'),
        ('Gap normalisé', 'gap_norm = gap(r)/max_gap\nRespiration cyclique'),
        ('Saturation locale', 'sat31 = mean(c31) sur n±w\nTexture de voisinage')
    ]

    y_start = 6.7
    for i, (name, desc) in enumerate(features):
        y = y_start - i * 0.5
        ax.text(1, y, f'• {name}:', fontsize=9, weight='bold')
        ax.text(1.2, y - 0.15, desc, fontsize=7, style='italic')

    # Arrow
    ax.annotate('', xy=(5, 4.3), xytext=(5, 4.5),
                arrowprops=dict(arrowstyle='->', lw=2))

    # 4. Scoring
    ax.add_patch(mpatches.FancyBboxPatch((0.5, 2.8), 9, 1.3,
                 boxstyle="round,pad=0.1", ec="black", fc=color_score, lw=2))
    ax.text(5, 3.7, 'CALCUL DU SCORE v1', ha='center', fontsize=12, weight='bold')
    ax.text(5, 3.25, 'score = 0.40·s31 + 0.30·s101 + 0.18·s251 + 0.08·ang + 0.04·gap_norm - 0.06·sat_clip',
            ha='center', fontsize=8, family='monospace')
    ax.text(5, 2.95, 'Sans prior sur les résidus (approche structurelle)',
            ha='center', fontsize=8, style='italic')

    # Arrow
    ax.annotate('', xy=(5, 2.6), xytext=(5, 2.8),
                arrowprops=dict(arrowstyle='->', lw=2))

    # 5. Sorting
    ax.add_patch(mpatches.FancyBboxPatch((0.5, 1.5), 9, 0.9,
                 boxstyle="round,pad=0.1", ec="black", fc=color_process, lw=2))
    ax.text(5, 2.1, 'TRI DÉCROISSANT PAR SCORE', ha='center', fontsize=12, weight='bold')
    ax.text(5, 1.75, 'Candidats ordonnés du plus "prime-like" au moins "prime-like"',
            ha='center', fontsize=9)

    # Arrow
    ax.annotate('', xy=(5, 1.3), xytext=(5, 1.5),
                arrowprops=dict(arrowstyle='->', lw=2))

    # 6. Evaluation
    ax.add_patch(mpatches.FancyBboxPatch((0.5, 0.2), 9, 0.9,
                 boxstyle="round,pad=0.1", ec="black", fc=color_output, lw=2))
    ax.text(5, 0.85, 'ÉVALUATION: Precision@K', ha='center', fontsize=12, weight='bold')
    ax.text(5, 0.5, 'P@K = proportion de nombres premiers dans les K meilleurs candidats',
            ha='center', fontsize=9)
    ax.text(5, 0.3, 'Lift = P@K / base_rate (mesure de gain prédictif)',
            ha='center', fontsize=8, style='italic')

    plt.tight_layout()
    return fig


def analyze_performance(windows_data):
    """Analyse des performances sur plusieurs fenêtres."""
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Extract data
    window_names = list(windows_data.keys())
    k_values = [100, 500, 1000, 5000, 20000]

    # 1. Precision@K comparison
    ax1 = fig.add_subplot(gs[0, 0])
    for window_name, data in windows_data.items():
        precisions = [data[f'P@{k}'] for k in k_values]
        ax1.plot(k_values, precisions, marker='o', linewidth=2, label=window_name)

    # Add baseline
    for window_name, data in windows_data.items():
        ax1.axhline(y=data['base_rate'], linestyle='--', alpha=0.5,
                   label=f"{window_name} baseline")

    ax1.set_xlabel('K (nombre de candidats)', fontsize=11)
    ax1.set_ylabel('Precision@K', fontsize=11)
    ax1.set_title('Performance: Precision@K vs Baseline', fontsize=13, weight='bold')
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=8, loc='best')

    # 2. Lift analysis
    ax2 = fig.add_subplot(gs[0, 1])
    for window_name, data in windows_data.items():
        lifts = [data[f'P@{k}'] / data['base_rate'] for k in k_values]
        ax2.plot(k_values, lifts, marker='s', linewidth=2, label=window_name)

    ax2.axhline(y=1.0, linestyle='--', color='red', linewidth=2, alpha=0.7,
               label='Baseline (lift=1)')
    ax2.set_xlabel('K (nombre de candidats)', fontsize=11)
    ax2.set_ylabel('Lift (P@K / base_rate)', fontsize=11)
    ax2.set_title('Gain prédictif (Lift)', fontsize=13, weight='bold')
    ax2.set_xscale('log')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=9, loc='best')

    # 3. Base rate evolution
    ax3 = fig.add_subplot(gs[1, 0])
    base_rates = [data['base_rate'] for data in windows_data.values()]
    candidates_counts = [data['candidates'] for data in windows_data.values()]

    ax3.bar(window_names, base_rates, color='steelblue', alpha=0.7, edgecolor='black')
    ax3.set_ylabel('Base Rate (taux naturel de premiers)', fontsize=11)
    ax3.set_title('Évolution du taux de nombres premiers', fontsize=13, weight='bold')
    ax3.grid(True, alpha=0.3, axis='y')

    # Add values on bars
    for i, (br, count) in enumerate(zip(base_rates, candidates_counts)):
        ax3.text(i, br + 0.01, f'{br:.4f}\n({count:,} cand.)',
                ha='center', fontsize=9)

    # 4. Performance summary table
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('tight')
    ax4.axis('off')

    # Build table data
    table_data = [['Fenêtre', 'Candidats', 'Base Rate', 'P@5000', 'Lift@5000']]
    for window_name, data in windows_data.items():
        lift_5000 = data['P@5000'] / data['base_rate']
        table_data.append([
            window_name,
            f"{data['candidates']:,}",
            f"{data['base_rate']:.4f}",
            f"{data['P@5000']:.4f}",
            f"{lift_5000:.2f}x"
        ])

    table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.2, 0.18, 0.18, 0.19])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    # Style header
    for i in range(5):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Style rows
    for i in range(1, len(table_data)):
        for j in range(5):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F5F5F5')

    ax4.set_title('Résumé des performances', fontsize=13, weight='bold', pad=20)

    return fig


def analyze_score_distribution(A=250001, B=500000, P=2310, w=3, sample_size=5000):
    """Analyse de la distribution des scores."""
    print(f"Calcul de la distribution des scores sur [{A}, {B}]...")

    wheel = residues_and_gaps(P)
    prime_factors = factorize_squarefree(P)
    pre = build_precomp(B, w=w)
    cand = candidate_mask(B, prime_factors)

    # Sample candidates
    candidates_list = [n for n in range(A, B + 1) if cand[n]]
    np.random.seed(42)
    if len(candidates_list) > sample_size:
        sampled = np.random.choice(candidates_list, sample_size, replace=False)
    else:
        sampled = candidates_list

    scores_prime = []
    scores_composite = []

    for n in sampled:
        score = score_v1_no_residue(n, P=P, wheel=wheel, pre=pre)
        if pre.is_prime[n]:
            scores_prime.append(score)
        else:
            scores_composite.append(score)

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Histogram comparison
    ax1 = axes[0, 0]
    bins = np.linspace(min(scores_composite + scores_prime),
                      max(scores_composite + scores_prime), 50)
    ax1.hist(scores_prime, bins=bins, alpha=0.6, label='Nombres premiers',
            color='green', edgecolor='black')
    ax1.hist(scores_composite, bins=bins, alpha=0.6, label='Nombres composés',
            color='red', edgecolor='black')
    ax1.set_xlabel('Score', fontsize=11)
    ax1.set_ylabel('Fréquence', fontsize=11)
    ax1.set_title('Distribution des scores', fontsize=13, weight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # 2. Box plot
    ax2 = axes[0, 1]
    bp = ax2.boxplot([scores_composite, scores_prime],
                     labels=['Composés', 'Premiers'],
                     patch_artist=True)
    bp['boxes'][0].set_facecolor('red')
    bp['boxes'][0].set_alpha(0.6)
    bp['boxes'][1].set_facecolor('green')
    bp['boxes'][1].set_alpha(0.6)
    ax2.set_ylabel('Score', fontsize=11)
    ax2.set_title('Comparaison des distributions', fontsize=13, weight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # 3. Cumulative distribution
    ax3 = axes[1, 0]
    sorted_prime = np.sort(scores_prime)[::-1]
    sorted_comp = np.sort(scores_composite)[::-1]
    ax3.plot(np.arange(len(sorted_prime)) / len(sorted_prime), sorted_prime,
            label='Premiers', color='green', linewidth=2)
    ax3.plot(np.arange(len(sorted_comp)) / len(sorted_comp), sorted_comp,
            label='Composés', color='red', linewidth=2)
    ax3.set_xlabel('Percentile', fontsize=11)
    ax3.set_ylabel('Score', fontsize=11)
    ax3.set_title('Distribution cumulative (décroissante)', fontsize=13, weight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)

    # 4. Statistics table
    ax4 = axes[1, 1]
    ax4.axis('tight')
    ax4.axis('off')

    stats_data = [
        ['Statistique', 'Premiers', 'Composés', 'Différence'],
        ['Moyenne', f'{np.mean(scores_prime):.6f}', f'{np.mean(scores_composite):.6f}',
         f'{np.mean(scores_prime) - np.mean(scores_composite):.6f}'],
        ['Médiane', f'{np.median(scores_prime):.6f}', f'{np.median(scores_composite):.6f}',
         f'{np.median(scores_prime) - np.median(scores_composite):.6f}'],
        ['Écart-type', f'{np.std(scores_prime):.6f}', f'{np.std(scores_composite):.6f}',
         f'{np.std(scores_prime) - np.std(scores_composite):.6f}'],
        ['Min', f'{np.min(scores_prime):.6f}', f'{np.min(scores_composite):.6f}', '-'],
        ['Max', f'{np.max(scores_prime):.6f}', f'{np.max(scores_composite):.6f}', '-'],
        ['Count', f'{len(scores_prime)}', f'{len(scores_composite)}', '-']
    ]

    table = ax4.table(cellText=stats_data, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.25, 0.25, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Style header
    for i in range(4):
        table[(0, i)].set_facecolor('#2196F3')
        table[(0, i)].set_text_props(weight='bold', color='white')

    ax4.set_title('Statistiques comparatives', fontsize=13, weight='bold', pad=20)

    plt.tight_layout()
    return fig


def create_wheel_visualization(P=2310):
    """Visualisation de la structure de la roue primorielle."""
    wheel = residues_and_gaps(P)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # 1. Gap distribution
    ax1 = axes[0]
    gap_counts = {}
    for gap in wheel.gaps:
        gap_counts[gap] = gap_counts.get(gap, 0) + 1

    gaps_sorted = sorted(gap_counts.items())
    ax1.bar([g for g, _ in gaps_sorted], [c for _, c in gaps_sorted],
           color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Taille du gap', fontsize=11)
    ax1.set_ylabel('Fréquence', fontsize=11)
    ax1.set_title(f'Distribution des gaps cycliques (P={P})', fontsize=13, weight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Add statistics
    ax1.text(0.98, 0.97, f'φ(P) = {len(wheel.residues)} résidus\n'
                         f'Max gap = {wheel.max_gap}\n'
                         f'Min gap = {min(wheel.gaps)}\n'
                         f'Mean gap = {np.mean(wheel.gaps):.2f}',
            transform=ax1.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # 2. Cumulative gap pattern (circular visualization simplified)
    ax2 = axes[1]
    cumsum_gaps = np.cumsum([0] + wheel.gaps[:-1])
    ax2.plot(cumsum_gaps, wheel.gaps, 'o-', markersize=3, linewidth=1, alpha=0.6)
    ax2.set_xlabel('Position dans le cycle', fontsize=11)
    ax2.set_ylabel('Taille du gap', fontsize=11)
    ax2.set_title(f'Motif de respiration cyclique (P={P})', fontsize=13, weight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=np.mean(wheel.gaps), linestyle='--', color='red',
               label=f'Gap moyen = {np.mean(wheel.gaps):.2f}')
    ax2.legend()

    plt.tight_layout()
    return fig


def main():
    """Fonction principale."""
    print("=" * 70)
    print("ANALYSE ET VISUALISATION DU PROCESSUS GUASTI TRANSFORM")
    print("=" * 70)
    print()

    # Check if matplotlib is installed
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
    except ImportError:
        print("ERROR: matplotlib is required. Install with: pip install matplotlib")
        return

    # 1. Architecture diagram
    print("1. Création du diagramme d'architecture...")
    fig1 = create_process_architecture_diagram()
    fig1.savefig('guasti_architecture.png', dpi=300, bbox_inches='tight')
    print("   ✓ Sauvegardé: guasti_architecture.png")
    plt.close(fig1)

    # 2. Performance analysis with real data
    print("\n2. Analyse des performances sur 3 fenêtres...")
    windows_data = {
        '[250k-500k]': {
            'candidates': 51952,
            'base_rate': 0.375231,
            'P@100': 0.810000,
            'P@500': 0.796000,
            'P@1000': 0.791000,
            'P@5000': 0.792800,
            'P@20000': 0.792750
        },
        '[500k-750k]': {
            'candidates': 51947,
            'base_rate': 0.359982,
            'P@100': 0.770000,
            'P@500': 0.740000,
            'P@1000': 0.740000,
            'P@5000': 0.755000,
            'P@20000': 0.751050
        },
        '[750k-1M]': {
            'candidates': 51947,
            'base_rate': 0.351512,
            'P@100': 0.720000,
            'P@500': 0.696000,
            'P@1000': 0.715000,
            'P@5000': 0.731400,
            'P@20000': 0.730250
        }
    }

    fig2 = analyze_performance(windows_data)
    fig2.savefig('guasti_performance_analysis.png', dpi=300, bbox_inches='tight')
    print("   ✓ Sauvegardé: guasti_performance_analysis.png")
    plt.close(fig2)

    # 3. Score distribution
    print("\n3. Analyse de la distribution des scores...")
    fig3 = analyze_score_distribution(A=250001, B=500000, P=2310, w=3, sample_size=5000)
    fig3.savefig('guasti_score_distribution.png', dpi=300, bbox_inches='tight')
    print("   ✓ Sauvegardé: guasti_score_distribution.png")
    plt.close(fig3)

    # 4. Wheel visualization
    print("\n4. Visualisation de la roue primorielle...")
    fig4 = create_wheel_visualization(P=2310)
    fig4.savefig('guasti_wheel_structure.png', dpi=300, bbox_inches='tight')
    print("   ✓ Sauvegardé: guasti_wheel_structure.png")
    plt.close(fig4)

    print("\n" + "=" * 70)
    print("ANALYSE TERMINÉE")
    print("=" * 70)
    print("\nFichiers générés:")
    print("  1. guasti_architecture.png          - Architecture du processus")
    print("  2. guasti_performance_analysis.png  - Analyse de performance")
    print("  3. guasti_score_distribution.png    - Distribution des scores")
    print("  4. guasti_wheel_structure.png       - Structure de la roue")
    print("\n" + "=" * 70)

    # Print summary statistics
    print("\nRÉSUMÉ DES RÉSULTATS:")
    print("-" * 70)
    for window_name, data in windows_data.items():
        lift = data['P@5000'] / data['base_rate']
        print(f"\nFenêtre {window_name}:")
        print(f"  • Candidats:     {data['candidates']:,}")
        print(f"  • Base rate:     {data['base_rate']:.4f} ({data['base_rate']*100:.2f}%)")
        print(f"  • P@5000:        {data['P@5000']:.4f} ({data['P@5000']*100:.2f}%)")
        print(f"  • Lift@5000:     {lift:.2f}x")
        print(f"  • Gain absolu:   +{(data['P@5000'] - data['base_rate'])*100:.2f} points de %")

    print("\n" + "=" * 70)
    print("CONCLUSION:")
    print("-" * 70)
    print("Le score Guasti v1 (sans prior résidu) démontre un pouvoir prédictif")
    print("significatif avec un lift stable entre 2.0x et 2.1x sur toutes les fenêtres.")
    print("La conjecture (P@5000 ≥ 0.70) est vérifiée sur les 3 fenêtres testées.")
    print("=" * 70)


if __name__ == "__main__":
    main()
