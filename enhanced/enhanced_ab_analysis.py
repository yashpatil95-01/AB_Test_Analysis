"""
Enhanced A/B Test Analysis with Data Visualizations and Business Insights
Author: Enhanced by AI Assistant
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from scipy import stats
import warnings
import os
warnings.filterwarnings('ignore')

# Set style for better visualizations
try:
    plt.style.use('seaborn-v0_8')
except:
    plt.style.use('seaborn')
sns.set_palette("husl")

class ABTestAnalyzer:
    def __init__(self, data_path):
        """Initialize the AB Test Analyzer with data"""
        self.df = pd.read_csv(data_path)
        self.results = {}
        
    def load_and_explore_data(self):
        """Load and perform initial data exploration"""
        print("="*60)
        print("A/B TEST ANALYSIS - DATA EXPLORATION")
        print("="*60)
        
        print(f"Dataset Shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        print("\nFirst 5 rows:")
        print(self.df.head())
        
        print("\nDataset Info:")
        print(self.df.info())
        
        print("\nMissing Values:")
        print(self.df.isnull().sum())
        
        print("\nGroup Distribution:")
        print(self.df['Group'].value_counts())
        
        print("\nConversion Distribution:")
        print(self.df['Conversion'].value_counts())
        
        return self.df
    
    def calculate_basic_metrics(self):
        """Calculate basic conversion metrics for both groups"""
        print("\n" + "="*60)
        print("BASIC CONVERSION METRICS")
        print("="*60)
        
        # Convert Yes/No to 1/0
        self.df['Conversion_Binary'] = self.df['Conversion'].map({'Yes': 1, 'No': 0})
        
        # Group-wise metrics
        group_stats = self.df.groupby('Group').agg({
            'Conversion_Binary': ['count', 'sum', 'mean'],
            'Page Views': ['mean', 'median', 'std'],
            'Time Spent': ['mean', 'median', 'std']
        }).round(4)
        
        print("Group-wise Statistics:")
        print(group_stats)
        
        # Store results
        group_a = self.df[self.df['Group'] == 'A']['Conversion_Binary']
        group_b = self.df[self.df['Group'] == 'B']['Conversion_Binary']
        
        self.results['group_a_conversions'] = group_a.sum()
        self.results['group_a_total'] = group_a.count()
        self.results['group_a_rate'] = group_a.mean()
        
        self.results['group_b_conversions'] = group_b.sum()
        self.results['group_b_total'] = group_b.count()
        self.results['group_b_rate'] = group_b.mean()
        
        self.results['lift'] = ((self.results['group_b_rate'] - self.results['group_a_rate']) / 
                               self.results['group_a_rate']) * 100
        
        print(f"\nGroup A Conversion Rate: {self.results['group_a_rate']:.4f} ({self.results['group_a_rate']*100:.2f}%)")
        print(f"Group B Conversion Rate: {self.results['group_b_rate']:.4f} ({self.results['group_b_rate']*100:.2f}%)")
        print(f"Relative Lift: {self.results['lift']:.2f}%")
        
        return group_stats
    
    def perform_statistical_tests(self):
        """Perform comprehensive statistical testing"""
        print("\n" + "="*60)
        print("STATISTICAL HYPOTHESIS TESTING")
        print("="*60)
        
        # Z-test for proportions
        count = [self.results['group_a_conversions'], self.results['group_b_conversions']]
        nobs = [self.results['group_a_total'], self.results['group_b_total']]
        
        stat, pval = proportions_ztest(count, nobs)
        
        # Confidence intervals
        ci_a = proportion_confint(self.results['group_a_conversions'], self.results['group_a_total'], alpha=0.05)
        ci_b = proportion_confint(self.results['group_b_conversions'], self.results['group_b_total'], alpha=0.05)
        
        # Effect size (Cohen's h)
        p1, p2 = self.results['group_a_rate'], self.results['group_b_rate']
        cohens_h = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))
        
        # Store results
        self.results['z_statistic'] = stat
        self.results['p_value'] = pval
        self.results['ci_a'] = ci_a
        self.results['ci_b'] = ci_b
        self.results['cohens_h'] = cohens_h
        
        print(f"Z-statistic: {stat:.4f}")
        print(f"P-value: {pval:.6f}")
        print(f"Cohen's h (Effect Size): {cohens_h:.4f}")
        print(f"Group A 95% CI: [{ci_a[0]:.4f}, {ci_a[1]:.4f}]")
        print(f"Group B 95% CI: [{ci_b[0]:.4f}, {ci_b[1]:.4f}]")
        
        # Statistical significance
        alpha = 0.05
        is_significant = pval < alpha
        self.results['is_significant'] = is_significant
        
        print(f"\nStatistical Significance (α = 0.05): {'YES' if is_significant else 'NO'}")
        
        return stat, pval
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("\n" + "="*60)
        print("CREATING VISUALIZATIONS")
        print("="*60)
        
        # Ensure results directory exists
        os.makedirs('PA-Projects/AB_Test_Analysis/results', exist_ok=True)
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Conversion Rate Comparison
        ax1 = plt.subplot(2, 3, 1)
        groups = ['Group A (Control)', 'Group B (Treatment)']
        rates = [self.results['group_a_rate']*100, self.results['group_b_rate']*100]
        colors = ['#FF6B6B', '#4ECDC4']
        
        bars = ax1.bar(groups, rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        ax1.set_ylabel('Conversion Rate (%)', fontsize=12)
        ax1.set_title('Conversion Rate Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, max(rates) * 1.2)
        
        # Add value labels on bars
        for bar, rate in zip(bars, rates):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{rate:.2f}%', ha='center', va='bottom', fontweight='bold')
        
        # 2. Sample Size Comparison
        ax2 = plt.subplot(2, 3, 2)
        sample_sizes = [self.results['group_a_total'], self.results['group_b_total']]
        bars2 = ax2.bar(groups, sample_sizes, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        ax2.set_ylabel('Sample Size', fontsize=12)
        ax2.set_title('Sample Size Distribution', fontsize=14, fontweight='bold')
        
        for bar, size in zip(bars2, sample_sizes):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'{size:,}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Confidence Intervals
        ax3 = plt.subplot(2, 3, 3)
        ci_lower = [self.results['ci_a'][0]*100, self.results['ci_b'][0]*100]
        ci_upper = [self.results['ci_a'][1]*100, self.results['ci_b'][1]*100]
        
        ax3.errorbar(groups, rates, 
                    yerr=[np.array(rates) - np.array(ci_lower), 
                          np.array(ci_upper) - np.array(rates)],
                    fmt='o', capsize=10, capthick=2, markersize=8, color='darkblue')
        ax3.set_ylabel('Conversion Rate (%)', fontsize=12)
        ax3.set_title('95% Confidence Intervals', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # 4. Page Views Distribution
        ax4 = plt.subplot(2, 3, 4)
        group_a_data = self.df[self.df['Group'] == 'A']['Page Views']
        group_b_data = self.df[self.df['Group'] == 'B']['Page Views']
        ax4.boxplot([group_a_data, group_b_data], labels=['Group A', 'Group B'])
        ax4.set_title('Page Views Distribution by Group', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Group', fontsize=12)
        ax4.set_ylabel('Page Views', fontsize=12)
        
        # 5. Time Spent Distribution
        ax5 = plt.subplot(2, 3, 5)
        group_a_time = self.df[self.df['Group'] == 'A']['Time Spent']
        group_b_time = self.df[self.df['Group'] == 'B']['Time Spent']
        ax5.boxplot([group_a_time, group_b_time], labels=['Group A', 'Group B'])
        ax5.set_title('Time Spent Distribution by Group', fontsize=14, fontweight='bold')
        ax5.set_xlabel('Group', fontsize=12)
        ax5.set_ylabel('Time Spent (seconds)', fontsize=12)
        
        # 6. Conversion by Device Type
        ax6 = plt.subplot(2, 3, 6)
        device_conversion = pd.crosstab(self.df['Device'], [self.df['Group'], self.df['Conversion']], normalize='index')
        device_conversion.plot(kind='bar', ax=ax6, color=['lightcoral', 'lightblue', 'lightgreen', 'lightyellow'])
        ax6.set_title('Conversion Rate by Device Type', fontsize=14, fontweight='bold')
        ax6.set_xlabel('Device Type', fontsize=12)
        ax6.set_ylabel('Conversion Rate', fontsize=12)
        ax6.legend(title='Group & Conversion', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax6.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('PA-Projects/AB_Test_Analysis/results/ab_test_visualizations.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        # Additional detailed visualizations
        self._create_detailed_analysis_plots()
    
    def _create_detailed_analysis_plots(self):
        """Create additional detailed analysis plots"""
        
        # Conversion funnel analysis
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Geographic Analysis
        geo_analysis = self.df.groupby(['Location', 'Group'])['Conversion_Binary'].agg(['count', 'sum', 'mean']).reset_index()
        geo_pivot = geo_analysis.pivot(index='Location', columns='Group', values='mean')
        geo_pivot.plot(kind='bar', ax=ax1, color=['#FF6B6B', '#4ECDC4'])
        ax1.set_title('Conversion Rate by Geographic Location', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Conversion Rate', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend(title='Group')
        
        # 2. Page Views vs Conversion
        for group in ['A', 'B']:
            group_data = self.df[self.df['Group'] == group]
            converted = group_data[group_data['Conversion'] == 'Yes']['Page Views']
            not_converted = group_data[group_data['Conversion'] == 'No']['Page Views']
            
            ax2.hist(converted, alpha=0.7, label=f'Group {group} - Converted', bins=20)
            ax2.hist(not_converted, alpha=0.7, label=f'Group {group} - Not Converted', bins=20)
        
        ax2.set_title('Page Views Distribution: Converted vs Non-Converted', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Page Views', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.legend()
        
        # 3. Time Spent Analysis
        time_bins = pd.cut(self.df['Time Spent'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        time_conversion = pd.crosstab(time_bins, [self.df['Group'], self.df['Conversion']], normalize='index')
        time_conversion.plot(kind='bar', ax=ax3, stacked=True)
        ax3.set_title('Conversion Rate by Time Spent Categories', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Time Spent Categories', fontsize=12)
        ax3.set_ylabel('Conversion Rate', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Statistical Power Analysis
        effect_sizes = np.linspace(0, 0.1, 100)
        sample_size = self.results['group_a_total']
        
        powers = []
        for effect in effect_sizes:
            # Calculate power for each effect size
            power = stats.norm.cdf(stats.norm.ppf(0.975) - effect * np.sqrt(sample_size/2))
            powers.append(1 - power)
        
        ax4.plot(effect_sizes * 100, powers, linewidth=2, color='darkgreen')
        ax4.axhline(y=0.8, color='red', linestyle='--', label='80% Power')
        ax4.axvline(x=abs(self.results['group_b_rate'] - self.results['group_a_rate']) * 100, 
                   color='blue', linestyle='--', label='Observed Effect')
        ax4.set_title('Statistical Power Analysis', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Effect Size (%)', fontsize=12)
        ax4.set_ylabel('Statistical Power', fontsize=12)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('PA-Projects/AB_Test_Analysis/results/detailed_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_business_insights(self):
        """Generate comprehensive business insights and recommendations"""
        print("\n" + "="*80)
        print("BUSINESS INSIGHTS & RECOMMENDATIONS")
        print("="*80)
        
        # Calculate key business metrics
        absolute_lift = self.results['group_b_rate'] - self.results['group_a_rate']
        relative_lift = self.results['lift']
        
        # Statistical significance interpretation
        significance_level = "STATISTICALLY SIGNIFICANT" if self.results['is_significant'] else "NOT STATISTICALLY SIGNIFICANT"
        
        print(f"📊 EXECUTIVE SUMMARY")
        print(f"{'='*50}")
        print(f"• Test Duration: Based on {self.results['group_a_total'] + self.results['group_b_total']:,} total users")
        print(f"• Control Group (A): {self.results['group_a_rate']*100:.2f}% conversion rate")
        print(f"• Treatment Group (B): {self.results['group_b_rate']*100:.2f}% conversion rate")
        print(f"• Absolute Lift: {absolute_lift*100:.2f} percentage points")
        print(f"• Relative Lift: {relative_lift:.2f}%")
        print(f"• Statistical Significance: {significance_level}")
        print(f"• P-value: {self.results['p_value']:.6f}")
        
        print(f"\n🎯 BUSINESS IMPACT ANALYSIS")
        print(f"{'='*50}")
        
        if self.results['is_significant']:
            if relative_lift > 0:
                impact = "POSITIVE"
                recommendation = "IMPLEMENT"
                color = "🟢"
            else:
                impact = "NEGATIVE"
                recommendation = "DO NOT IMPLEMENT"
                color = "🔴"
        else:
            impact = "INCONCLUSIVE"
            recommendation = "CONTINUE TESTING"
            color = "🟡"
        
        print(f"{color} Impact Assessment: {impact}")
        print(f"{color} Recommendation: {recommendation}")
        
        # Detailed recommendations
        print(f"\n📈 DETAILED RECOMMENDATIONS")
        print(f"{'='*50}")
        
        if self.results['is_significant'] and relative_lift > 0:
            print("✅ RECOMMENDATION: IMPLEMENT THE NEW FEATURE")
            print("\nReasons:")
            print(f"• Statistically significant improvement of {relative_lift:.2f}%")
            print(f"• P-value ({self.results['p_value']:.6f}) is below significance threshold (0.05)")
            print(f"• Effect size (Cohen's h = {self.results['cohens_h']:.3f}) indicates meaningful difference")
            
            # Calculate potential business value
            if self.results['group_a_total'] > 0:
                monthly_users = 10000  # Assumption for business calculation
                additional_conversions = monthly_users * absolute_lift
                print(f"\n💰 PROJECTED BUSINESS VALUE:")
                print(f"• With {monthly_users:,} monthly users, expect {additional_conversions:.0f} additional conversions")
                print(f"• This represents a {relative_lift:.1f}% improvement in conversion rate")
        
        elif self.results['is_significant'] and relative_lift < 0:
            print("❌ RECOMMENDATION: DO NOT IMPLEMENT THE NEW FEATURE")
            print("\nReasons:")
            print(f"• Statistically significant decrease of {abs(relative_lift):.2f}%")
            print(f"• The new feature is harming conversion rates")
            print(f"• Consider investigating what aspects of the feature are causing the negative impact")
        
        else:
            print("⚠️ RECOMMENDATION: CONTINUE TESTING OR REDESIGN")
            print("\nReasons:")
            print(f"• Results are not statistically significant (p-value = {self.results['p_value']:.6f})")
            print(f"• Need larger sample size or longer test duration")
            print(f"• Consider improving the feature design before retesting")
        
        # Additional insights
        print(f"\n🔍 ADDITIONAL INSIGHTS")
        print(f"{'='*50}")
        
        # Device analysis
        device_analysis = self.df.groupby(['Device', 'Group'])['Conversion_Binary'].mean().unstack()
        print("📱 Device Performance:")
        for device in device_analysis.index:
            a_rate = device_analysis.loc[device, 'A'] * 100
            b_rate = device_analysis.loc[device, 'B'] * 100
            device_lift = ((b_rate - a_rate) / a_rate) * 100 if a_rate > 0 else 0
            print(f"   • {device}: A={a_rate:.1f}%, B={b_rate:.1f}% (Lift: {device_lift:+.1f}%)")
        
        # Geographic analysis
        geo_analysis = self.df.groupby(['Location', 'Group'])['Conversion_Binary'].mean().unstack()
        print("\n🌍 Geographic Performance:")
        for location in geo_analysis.index:
            a_rate = geo_analysis.loc[location, 'A'] * 100
            b_rate = geo_analysis.loc[location, 'B'] * 100
            geo_lift = ((b_rate - a_rate) / a_rate) * 100 if a_rate > 0 else 0
            print(f"   • {location}: A={a_rate:.1f}%, B={b_rate:.1f}% (Lift: {geo_lift:+.1f}%)")
        
        # Risk assessment
        print(f"\n⚠️ RISK ASSESSMENT")
        print(f"{'='*50}")
        
        ci_width_a = (self.results['ci_a'][1] - self.results['ci_a'][0]) * 100
        ci_width_b = (self.results['ci_b'][1] - self.results['ci_b'][0]) * 100
        
        print(f"• Confidence interval width - Group A: ±{ci_width_a/2:.2f}%")
        print(f"• Confidence interval width - Group B: ±{ci_width_b/2:.2f}%")
        
        if ci_width_a > 2 or ci_width_b > 2:
            print("• ⚠️ Wide confidence intervals suggest need for larger sample size")
        else:
            print("• ✅ Confidence intervals are reasonably narrow")
        
        # Implementation roadmap
        if self.results['is_significant'] and relative_lift > 0:
            print(f"\n🚀 IMPLEMENTATION ROADMAP")
            print(f"{'='*50}")
            print("1. 📋 Prepare rollout plan for gradual feature deployment")
            print("2. 📊 Set up monitoring dashboards to track post-launch performance")
            print("3. 🎯 Define success metrics and KPIs for ongoing measurement")
            print("4. 📈 Plan follow-up tests to optimize the feature further")
            print("5. 👥 Train customer support team on new feature functionality")
        
        return {
            'recommendation': recommendation,
            'impact': impact,
            'lift': relative_lift,
            'significance': self.results['is_significant']
        }
    
    def save_comprehensive_results(self):
        """Save comprehensive results to multiple formats"""
        
        # Ensure results directory exists
        os.makedirs('PA-Projects/AB_Test_Analysis/results', exist_ok=True)
        
        # Create detailed results dictionary
        detailed_results = {
            'Metric': [
                'Group A Sample Size', 'Group B Sample Size',
                'Group A Conversions', 'Group B Conversions', 
                'Group A Conversion Rate', 'Group B Conversion Rate',
                'Absolute Lift', 'Relative Lift (%)',
                'Z-Statistic', 'P-Value', 'Cohens h',
                'Group A CI Lower', 'Group A CI Upper',
                'Group B CI Lower', 'Group B CI Upper',
                'Statistical Significance', 'Recommendation'
            ],
            'Value': [
                self.results['group_a_total'], self.results['group_b_total'],
                self.results['group_a_conversions'], self.results['group_b_conversions'],
                f"{self.results['group_a_rate']:.4f}", f"{self.results['group_b_rate']:.4f}",
                f"{self.results['group_b_rate'] - self.results['group_a_rate']:.4f}",
                f"{self.results['lift']:.2f}%",
                f"{self.results['z_statistic']:.4f}", f"{self.results['p_value']:.6f}",
                f"{self.results['cohens_h']:.4f}",
                f"{self.results['ci_a'][0]:.4f}", f"{self.results['ci_a'][1]:.4f}",
                f"{self.results['ci_b'][0]:.4f}", f"{self.results['ci_b'][1]:.4f}",
                'Yes' if self.results['is_significant'] else 'No',
                'Implement' if self.results['is_significant'] and self.results['lift'] > 0 else 'Do Not Implement'
            ]
        }
        
        results_df = pd.DataFrame(detailed_results)
        results_df.to_csv('PA-Projects/AB_Test_Analysis/results/comprehensive_ab_results.csv', index=False)
        
        print(f"\n💾 Results saved to:")
        print(f"   • comprehensive_ab_results.csv")
        print(f"   • ab_test_visualizations.png") 
        print(f"   • detailed_analysis.png")

def main():
    """Main execution function"""
    
    # Initialize analyzer
    analyzer = ABTestAnalyzer('PA-Projects/AB_Test_Analysis/data/ab_testing.csv')
    
    # Run complete analysis
    analyzer.load_and_explore_data()
    analyzer.calculate_basic_metrics()
    analyzer.perform_statistical_tests()
    analyzer.create_visualizations()
    insights = analyzer.generate_business_insights()
    analyzer.save_comprehensive_results()
    
    print(f"\n" + "="*80)
    print("ANALYSIS COMPLETE! 🎉")
    print("="*80)
    print("Check the results folder for detailed outputs and visualizations.")

if __name__ == "__main__":
    main()