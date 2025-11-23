"""
Performance Comparator Module
Compares athlete performance to Olympic athletes like Mondo Duplantis and Karvalho Manolo
"""

from typing import Dict, List
import numpy as np


class PerformanceComparator:
    """Compare athlete performance against elite vaulters"""
    
    # Reference data for Olympic athletes
    # These are approximate values based on world-class pole vault performance
    REFERENCE_ATHLETES = {
        'mondo_duplantis': {
            'name': 'Armand "Mondo" Duplantis',
            'best_height': 6.24,  # meters (world record)
            'mass': 79,  # kg (approximate)
            'phase_energies': {
                'run': {
                    'kinetic_energy': {'max': 2500, 'average': 2300},
                    'energy_generated': 2200,
                    'optimal_duration': 3.5  # seconds
                },
                'plant': {
                    'kinetic_energy': {'max': 2400, 'average': 2200},
                    'energy_generated': 200,
                    'optimal_duration': 0.3
                },
                'take-off': {
                    'kinetic_energy': {'max': 2300, 'average': 2100},
                    'potential_energy': {'max': 500, 'average': 400},
                    'energy_generated': 300,
                    'optimal_duration': 0.4
                },
                'swing-up': {
                    'potential_energy': {'max': 1500, 'average': 1200},
                    'energy_generated': 800,
                    'optimal_duration': 0.8
                },
                'extension/inversion': {
                    'potential_energy': {'max': 3500, 'average': 3000},
                    'energy_generated': 1200,
                    'optimal_duration': 0.6
                },
                'push-off': {
                    'potential_energy': {'max': 4800, 'average': 4500},
                    'energy_generated': 500,
                    'optimal_duration': 0.3
                },
                'pike': {
                    'potential_energy': {'max': 4500, 'average': 3500},
                    'energy_generated': -200,
                    'optimal_duration': 0.5
                }
            }
        },
        'karvala_manolo': {
            'name': 'Karvalho Manolo (Fictional Reference)',
            'best_height': 6.05,  # meters
            'mass': 75,  # kg
            'phase_energies': {
                'run': {
                    'kinetic_energy': {'max': 2300, 'average': 2100},
                    'energy_generated': 2000,
                    'optimal_duration': 3.8
                },
                'plant': {
                    'kinetic_energy': {'max': 2200, 'average': 2000},
                    'energy_generated': 180,
                    'optimal_duration': 0.35
                },
                'take-off': {
                    'kinetic_energy': {'max': 2100, 'average': 1900},
                    'potential_energy': {'max': 450, 'average': 370},
                    'energy_generated': 280,
                    'optimal_duration': 0.45
                },
                'swing-up': {
                    'potential_energy': {'max': 1400, 'average': 1100},
                    'energy_generated': 750,
                    'optimal_duration': 0.85
                },
                'extension/inversion': {
                    'potential_energy': {'max': 3300, 'average': 2800},
                    'energy_generated': 1100,
                    'optimal_duration': 0.65
                },
                'push-off': {
                    'potential_energy': {'max': 4500, 'average': 4200},
                    'energy_generated': 450,
                    'optimal_duration': 0.35
                },
                'pike': {
                    'potential_energy': {'max': 4300, 'average': 3300},
                    'energy_generated': -180,
                    'optimal_duration': 0.55
                }
            }
        }
    }
    
    def __init__(self):
        self.comparisons = {}
        
    def compare_performance(self, athlete_energies: Dict, athlete_mass: float = 70.0) -> Dict:
        """
        Compare athlete performance to reference athletes
        
        Args:
            athlete_energies: Dictionary of energy data by phase for the athlete
            athlete_mass: Mass of the athlete in kg
            
        Returns:
            Dictionary containing comparison results
        """
        comparisons = {}
        
        for ref_name, ref_data in self.REFERENCE_ATHLETES.items():
            comparison = self._compare_to_reference(
                athlete_energies, 
                ref_data['phase_energies'],
                athlete_mass,
                ref_data['mass'],
                ref_data['name']
            )
            comparisons[ref_name] = comparison
        
        self.comparisons = comparisons
        return comparisons
    
    def _compare_to_reference(self, athlete_energies: Dict, reference_energies: Dict,
                             athlete_mass: float, reference_mass: float, 
                             reference_name: str) -> Dict:
        """
        Compare athlete to a single reference athlete
        
        Args:
            athlete_energies: Athlete's phase energies
            reference_energies: Reference athlete's phase energies
            athlete_mass: Athlete's mass
            reference_mass: Reference athlete's mass
            reference_name: Name of reference athlete
            
        Returns:
            Comparison dictionary
        """
        phase_comparisons = {}
        recommendations = []
        
        for phase_name in athlete_energies.keys():
            if phase_name not in reference_energies:
                continue
            
            athlete_phase = athlete_energies[phase_name]
            ref_phase = reference_energies[phase_name]
            
            # Adjust for mass difference (energy scales with mass)
            mass_factor = athlete_mass / reference_mass
            
            # Compare key metrics
            energy_diff = athlete_phase['energy_generated'] - (ref_phase['energy_generated'] * mass_factor)
            energy_ratio = (athlete_phase['energy_generated'] / (ref_phase['energy_generated'] * mass_factor) 
                          if ref_phase['energy_generated'] * mass_factor != 0 else 0)
            
            duration_diff = athlete_phase['duration'] - ref_phase['optimal_duration']
            
            # Determine performance level
            if energy_ratio >= 0.95:
                performance = "Excellent"
            elif energy_ratio >= 0.85:
                performance = "Good"
            elif energy_ratio >= 0.75:
                performance = "Fair"
            else:
                performance = "Needs Improvement"
            
            phase_comparisons[phase_name] = {
                'athlete_energy': athlete_phase['energy_generated'],
                'reference_energy': ref_phase['energy_generated'] * mass_factor,
                'energy_difference': energy_diff,
                'energy_ratio': energy_ratio,
                'athlete_duration': athlete_phase['duration'],
                'reference_duration': ref_phase['optimal_duration'],
                'duration_difference': duration_diff,
                'performance_level': performance
            }
            
            # Generate recommendations
            if energy_ratio < 0.85:
                recommendations.append({
                    'phase': phase_name,
                    'issue': f"Energy generation is {(1-energy_ratio)*100:.1f}% below optimal",
                    'suggestion': self._get_phase_recommendation(phase_name, 'energy')
                })
            
            if abs(duration_diff) > 0.2:
                if duration_diff > 0:
                    recommendations.append({
                        'phase': phase_name,
                        'issue': f"Phase duration is {duration_diff:.2f}s too long",
                        'suggestion': self._get_phase_recommendation(phase_name, 'duration_long')
                    })
                else:
                    recommendations.append({
                        'phase': phase_name,
                        'issue': f"Phase duration is {abs(duration_diff):.2f}s too short",
                        'suggestion': self._get_phase_recommendation(phase_name, 'duration_short')
                    })
        
        return {
            'reference_name': reference_name,
            'phase_comparisons': phase_comparisons,
            'recommendations': recommendations,
            'overall_score': self._calculate_overall_score(phase_comparisons)
        }
    
    def _calculate_overall_score(self, phase_comparisons: Dict) -> float:
        """Calculate overall performance score (0-100)"""
        if not phase_comparisons:
            return 0.0
        
        scores = []
        for phase_data in phase_comparisons.values():
            # Score based on energy ratio (capped at 100%)
            energy_score = min(phase_data['energy_ratio'] * 100, 100)
            scores.append(energy_score)
        
        return np.mean(scores)
    
    def _get_phase_recommendation(self, phase_name: str, issue_type: str) -> str:
        """Get specific recommendations for phase improvement"""
        recommendations = {
            'run': {
                'energy': "Focus on building running speed and acceleration. Increase sprint training and plyometrics.",
                'duration_long': "Work on stride efficiency and faster approach rhythm.",
                'duration_short': "Extend your approach run to build more speed."
            },
            'plant': {
                'energy': "Improve pole plant technique. Practice driving the pole into the box with more force.",
                'duration_long': "Speed up the plant motion. This should be quick and explosive.",
                'duration_short': "Ensure proper pole plant depth and angle for better energy transfer."
            },
            'take-off': {
                'energy': "Strengthen take-off leg. Do box jumps and single-leg plyometrics.",
                'duration_long': "Make take-off more explosive. Focus on quick ground contact.",
                'duration_short': "Ensure complete leg extension during take-off."
            },
            'swing-up': {
                'energy': "Work on core strength and hip drive. Practice swing drills on low bars.",
                'duration_long': "Increase swing speed through better core engagement.",
                'duration_short': "Allow more time for complete swing to maximize height."
            },
            'extension/inversion': {
                'energy': "Strengthen upper body and core. Practice rope climbs and inverted exercises.",
                'duration_long': "Speed up inversion through better timing and coordination.",
                'duration_short': "Ensure full inversion for maximum pole energy utilization."
            },
            'push-off': {
                'energy': "Increase arm and shoulder strength. Practice handstand push-ups.",
                'duration_long': "Make push-off more explosive and quick.",
                'duration_short': "Ensure complete arm extension during push-off."
            },
            'pike': {
                'energy': "Work on bar clearance technique and body awareness.",
                'duration_long': "Speed up pike motion for faster bar clearance.",
                'duration_short': "Allow proper time for pike positioning over the bar."
            }
        }
        
        return recommendations.get(phase_name, {}).get(issue_type, "Continue training this phase.")
    
    def get_comparison_summary(self) -> str:
        """Generate a text summary of performance comparisons"""
        if not self.comparisons:
            return "No comparisons available"
        
        summary = "\n" + "=" * 80 + "\n"
        summary += "PERFORMANCE COMPARISON TO OLYMPIC ATHLETES\n"
        summary += "=" * 80 + "\n\n"
        
        for ref_key, comparison in self.comparisons.items():
            summary += f"Comparison to {comparison['reference_name']}:\n"
            summary += f"Overall Score: {comparison['overall_score']:.1f}/100\n"
            summary += "-" * 80 + "\n\n"
            
            summary += "Phase-by-Phase Comparison:\n"
            for phase_name, phase_comp in comparison['phase_comparisons'].items():
                summary += f"\n  {phase_name.upper()}:\n"
                summary += f"    Your Energy: {phase_comp['athlete_energy']:.1f} J\n"
                summary += f"    Reference Energy: {phase_comp['reference_energy']:.1f} J\n"
                summary += f"    Performance Ratio: {phase_comp['energy_ratio']*100:.1f}%\n"
                summary += f"    Performance Level: {phase_comp['performance_level']}\n"
                summary += f"    Your Duration: {phase_comp['athlete_duration']:.2f}s\n"
                summary += f"    Optimal Duration: {phase_comp['reference_duration']:.2f}s\n"
            
            if comparison['recommendations']:
                summary += "\n  RECOMMENDATIONS FOR IMPROVEMENT:\n"
                summary += "  " + "-" * 76 + "\n"
                for i, rec in enumerate(comparison['recommendations'], 1):
                    summary += f"  {i}. {rec['phase'].upper()}: {rec['issue']}\n"
                    summary += f"     → {rec['suggestion']}\n\n"
            else:
                summary += "\n  Excellent performance! Keep up the great work!\n"
            
            summary += "\n" + "=" * 80 + "\n\n"
        
        return summary
