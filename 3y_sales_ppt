import React, { useState, useEffect } from 'react';
import { ChevronRight, ChevronLeft, TrendingUp, Users, AlertCircle, Target, Award, ArrowRight, BarChart2, PieChart, Activity, DollarSign, Briefcase, Grid, Monitor } from 'lucide-react';

// --- Components ---

// 1. Custom Button Component
const Button = ({ children, onClick, variant = 'primary', className = '' }) => {
  const baseStyle = "px-6 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2";
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 shadow-lg hover:shadow-blue-500/30",
    secondary: "bg-slate-700 text-slate-200 hover:bg-slate-600",
    outline: "border border-slate-600 text-slate-400 hover:border-slate-400 hover:text-white"
  };
  return (
    <button onClick={onClick} className={`${baseStyle} ${variants[variant]} ${className}`}>
      {children}
    </button>
  );
};

// 2. Custom Card
const Card = ({ children, className = '' }) => (
  <div className={`bg-slate-800/50 backdrop-blur-md border border-slate-700 rounded-xl p-6 shadow-xl ${className}`}>
    {children}
  </div>
);

// --- Chart Components (SVG based for zero dependencies) ---

// Radar Chart Component (Fixed Logic & Layout)
const RadarChart = ({ data }) => {
  // data: { label: string, A: number, B: number }[] (Scale 0-100)
  const size = 300;
  const center = size / 2;
  const radius = 90; // Reduced slightly to fit labels
  const angleSlice = (Math.PI * 2) / data.length;

  const getCoordinates = (value, index) => {
    const angle = index * angleSlice - Math.PI / 2;
    return [
      center + (Math.cos(angle) * radius * value) / 100,
      center + (Math.sin(angle) * radius * value) / 100
    ];
  };

  const pathA = data.map((d, i) => getCoordinates(d.A, i)).join("L") + "Z";
  const pathB = data.map((d, i) => getCoordinates(d.B, i)).join("L") + "Z";

  // Background Grid Path
  const getGridPath = (scale) => {
    return data.map((_, i) => getCoordinates(scale, i)).join("L") + "Z";
  };

  return (
    <div className="relative flex flex-col items-center w-full h-full justify-center">
      <svg width={size} height={size} className="overflow-visible">
        {/* Background Grids */}
        {[20, 40, 60, 80, 100].map(scale => (
          <path key={scale} d={getGridPath(scale)} fill="none" stroke="#334155" strokeWidth="1" strokeDasharray={scale === 100 ? "0" : "4 4"} />
        ))}
        
        {/* Axes */}
        {data.map((d, i) => {
          const [x, y] = getCoordinates(100, i);
          const angle = index => index * angleSlice - Math.PI / 2;
          
          // Better label positioning logic
          const labelX = center + (Math.cos(angle(i)) * (radius + 25)); 
          const labelY = center + (Math.sin(angle(i)) * (radius + 15));
          const anchor = Math.abs(x - center) < 10 ? "middle" : x > center ? "start" : "end";

          return (
            <g key={i}>
              <line x1={center} y1={center} x2={x} y2={y} stroke="#334155" />
              <text 
                x={labelX} 
                y={labelY} 
                textAnchor={anchor} 
                dominantBaseline="middle"
                fill="#94a3b8" 
                fontSize="11" 
                fontWeight="bold"
              >
                {d.label}
              </text>
            </g>
          );
        })}
        
        {/* Data Paths */}
        <path d={pathA} fill="rgba(59, 130, 246, 0.2)" stroke="#3b82f6" strokeWidth="2" />
        <path d={pathB} fill="rgba(239, 68, 68, 0.2)" stroke="#ef4444" strokeWidth="2" />
        
        {/* Data Points */}
        {data.map((d, i) => {
             const [ax, ay] = getCoordinates(d.A, i);
             const [bx, by] = getCoordinates(d.B, i);
             return (
                 <g key={i}>
                    <circle cx={ax} cy={ay} r="3" fill="#3b82f6" />
                    <circle cx={bx} cy={by} r="3" fill="#ef4444" />
                 </g>
             )
        })}
      </svg>
      <div className="flex gap-6 mt-4">
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-blue-500 rounded-full"></div><span className="text-sm text-slate-300">재직자 평균</span></div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-red-500 rounded-full"></div><span className="text-sm text-slate-300">이탈자 평균</span></div>
      </div>
    </div>
  );
};

// Heatmap Component
const Heatmap = () => {
  // Mock Data: X=Tenure (Months), Y=Performance Grade (S, A, B, C, D)
  // Value = Turnover Probability (Color intensity)
  const xLabels = ['1-3개월', '4-6개월', '7-12개월', '13-24개월', '25-36개월'];
  const yLabels = ['S등급', 'A등급', 'B등급', 'C등급', 'D등급'];
  const data = [
    [5, 10, 15, 20, 10], // S
    [10, 20, 30, 40, 25], // A
    [20, 30, 40, 30, 20], // B
    [40, 60, 50, 20, 15], // C
    [80, 90, 70, 40, 30]  // D - High turnover early
  ];

  const getColor = (val) => {
    if (val >= 70) return 'bg-red-600';
    if (val >= 50) return 'bg-red-500';
    if (val >= 30) return 'bg-orange-500';
    if (val >= 15) return 'bg-yellow-500';
    return 'bg-emerald-500';
  };

  return (
    <div className="w-full">
      <div className="grid grid-cols-6 gap-1 mb-2">
        <div className="text-xs text-slate-400 text-right pr-2"></div>
        {xLabels.map((l, i) => <div key={i} className="text-xs text-slate-400 text-center font-bold">{l}</div>)}
      </div>
      {yLabels.map((y, i) => (
        <div key={i} className="grid grid-cols-6 gap-1 mb-1 items-center">
          <div className="text-xs text-slate-300 text-right pr-2 font-bold">{y}</div>
          {data[i].map((val, j) => (
            <div key={j} className={`h-12 rounded flex items-center justify-center text-xs font-bold text-white transition-all hover:scale-105 cursor-pointer group relative ${getColor(val)}`}>
              {val}%
              <div className="absolute bottom-full mb-2 hidden group-hover:block bg-slate-900 text-xs p-2 rounded z-10 whitespace-nowrap border border-slate-700">
                이탈률: {val}%<br/>주요사유: {val > 60 ? '성과 압박 & 부적응' : val > 30 ? '보상 불만' : '자연 이탈'}
              </div>
            </div>
          ))}
        </div>
      ))}
      <div className="mt-4 flex justify-between items-center text-xs text-slate-400">
        <span>* Y축: 성과 등급 / X축: 근속 기간</span>
        <div className="flex gap-2">
          <span className="flex items-center gap-1"><div className="w-3 h-3 bg-emerald-500 rounded"></div>안정</span>
          <span className="flex items-center gap-1"><div className="w-3 h-3 bg-yellow-500 rounded"></div>주의</span>
          <span className="flex items-center gap-1"><div className="w-3 h-3 bg-red-600 rounded"></div>위험</span>
        </div>
      </div>
    </div>
  );
};

// Scatter/Bubble Chart Component (Fixed Axis & Layout with Ticks)
const BubbleChart = () => {
  // Mock Data: x=Performance, y=Incentive Satisfaction, z=Tenure(size), c=Status
  const points = [
    { x: 90, y: 80, z: 30, status: 'stay', label: 'High Perf / High Pay' },
    { x: 85, y: 30, z: 20, status: 'leave', label: 'High Perf / Low Pay (Risk)' },
    { x: 40, y: 40, z: 10, status: 'leave', label: 'Low Perf / Low Pay' },
    { x: 60, y: 70, z: 25, status: 'stay', label: 'Mid Perf / Good Pay' },
    { x: 95, y: 20, z: 15, status: 'leave', label: 'Top Talent Burnout' },
    { x: 50, y: 50, z: 28, status: 'stay', label: 'Average' },
    { x: 30, y: 80, z: 5, status: 'stay', label: 'Overpaid Low Perf' },
  ];

  // Ticks for axis (0, 20, 40, 60, 80, 100)
  const ticks = [0, 20, 40, 60, 80, 100];

  return (
    <div className="relative h-72 w-full pl-12 pb-12"> {/* Increased padding for scale numbers */}
      {/* Chart Area */}
      <div className="absolute inset-0 left-12 bottom-12 border-l border-b border-slate-400"> {/* Brighter border color */}
        
        {/* Y-Axis Ticks & Grid */}
        {ticks.map((tick) => (
          <div key={`y-${tick}`} className="absolute w-full flex items-center" style={{ bottom: `${tick}%` }}>
             {/* Grid line (optional, kept subtle) */}
             <div className="w-full border-t border-slate-700/30 absolute left-0"></div>
             {/* Tick Label */}
             <span className="absolute -left-8 text-xs font-bold text-slate-300 w-6 text-right">{tick}</span>
             {/* Tick Mark */}
             <div className="absolute -left-1 w-1 h-px bg-slate-400"></div>
          </div>
        ))}

        {/* X-Axis Ticks */}
        {ticks.map((tick) => (
          <div key={`x-${tick}`} className="absolute h-full flex flex-col justify-end items-center" style={{ left: `${tick}%` }}>
             {/* Grid line (optional) */}
             <div className="h-full border-l border-slate-700/30 absolute bottom-0"></div>
             {/* Tick Label */}
             <span className="absolute -bottom-6 text-xs font-bold text-slate-300 transform -translate-x-1/2">{tick}</span>
             {/* Tick Mark */}
             <div className="absolute -bottom-1 h-1 w-px bg-slate-400"></div>
          </div>
        ))}

        {/* Data Points */}
        {points.map((p, i) => (
          <div
            key={i}
            className={`absolute rounded-full flex items-center justify-center border-2 transition-all hover:scale-125 cursor-pointer group ${p.status === 'leave' ? 'border-red-400 bg-red-500/30' : 'border-blue-400 bg-blue-500/30'}`} // Brighter bubble colors
            style={{
              left: `${p.x}%`,
              bottom: `${p.y}%`,
              width: `${Math.max(20, p.z)}px`,
              height: `${Math.max(20, p.z)}px`,
              transform: 'translate(-50%, 50%)'
            }}
          >
            <div className="absolute bottom-full mb-1 hidden group-hover:block bg-slate-900 text-xs p-2 rounded z-20 whitespace-nowrap border border-slate-700 shadow-xl">
              <span className="font-bold text-white">{p.label}</span><br/>
              <span className="text-slate-400">성과: {p.x}점 / 만족도: {p.y}점</span>
            </div>
          </div>
        ))}
        
        {/* Quadrant Guidelines (Midpoint 50) */}
        <div className="absolute top-0 bottom-0 left-1/2 border-l-2 border-dashed border-slate-600 opacity-50"></div>
        <div className="absolute left-0 right-0 top-1/2 border-t-2 border-dashed border-slate-600 opacity-50"></div>
      </div>

      {/* Axis Labels */}
      <div className="absolute bottom-0 right-0 text-sm font-black text-slate-200">성과 점수 (Performance) →</div>
      <div className="absolute left-0 top-0 -rotate-90 origin-top-right -translate-x-full text-sm font-black text-slate-200 whitespace-nowrap">보상 만족도 (Incentive) →</div>
      
      {/* Quadrant Labels */}
      <div className="absolute top-4 right-4 text-xs text-blue-300 font-bold opacity-80 text-right bg-slate-900/80 p-1 rounded border border-blue-500/30">Core Talent<br/>(High/High)</div>
      <div className="absolute bottom-16 right-4 text-xs text-red-300 font-bold opacity-80 text-right bg-slate-900/80 p-1 rounded border border-red-500/30">Risk Zone<br/>(High/Low)</div>
    </div>
  );
};


// --- Slides ---

const Slide1_Title = () => (
  <div className="flex flex-col items-center justify-center h-full text-center space-y-8 animate-fade-in">
    <div className="inline-flex items-center justify-center p-4 bg-blue-500/10 rounded-full mb-4 ring-2 ring-blue-500/50">
      <TrendingUp size={48} className="text-blue-400" />
    </div>
    <h1 className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-blue-100 to-slate-400 mb-4 leading-tight">
      Sales 부서 저년차 직원<br />이탈 요인 심층 분석
    </h1>
    <p className="text-xl text-slate-400 max-w-2xl">
      성과(Performance) 데이터를 중심으로 한 3년 이하 근속자 Retention 전략
    </p>
  </div>
);

const Slide2_Hypothesis = () => (
  <div className="h-full flex flex-col justify-center px-12">
    <div className="mb-8 border-l-4 border-blue-500 pl-6">
      <h2 className="text-3xl font-bold text-white mb-2">분석 배경 및 가설</h2>
      <p className="text-slate-400">왜 3년차 이하인가? 왜 성과인가?</p>
    </div>

    <div className="grid grid-cols-2 gap-8">
      <Card className="hover:bg-slate-800 transition-colors">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-red-500/10 rounded-lg text-red-400"><AlertCircle size={24} /></div>
          <div>
            <h3 className="text-xl font-bold text-slate-200 mb-2">Problem</h3>
            <p className="text-slate-400 leading-relaxed">
              최근 1년간 Sales 부서 3년차 이하 직원의 이탈률이 
              <span className="text-red-400 font-bold mx-1">28%</span>로 
              전사 평균(12%)을 크게 상회함.
            </p>
          </div>
        </div>
      </Card>
      <Card className="hover:bg-slate-800 transition-colors">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-blue-500/10 rounded-lg text-blue-400"><Target size={24} /></div>
          <div>
            <h3 className="text-xl font-bold text-slate-200 mb-2">Hypothesis</h3>
            <p className="text-slate-400 leading-relaxed">
              "저년차 직원의 이탈은 단순 부적응이 아닌, 
              <span className="text-blue-400 font-bold mx-1">성과 압박과 보상 시스템의 괴리</span>에서 오는 구조적 문제일 것이다."
            </p>
          </div>
        </div>
      </Card>
    </div>

    <div className="mt-8 bg-slate-900/50 p-6 rounded-xl border border-dashed border-slate-700">
      <h4 className="text-sm font-bold text-slate-500 uppercase mb-4">Focus Areas</h4>
      <div className="flex justify-between text-slate-300">
        <div className="flex items-center gap-2"><ArrowRight size={16} className="text-blue-500"/> 온보딩 기간(0-6개월)의 성과 달성률</div>
        <div className="flex items-center gap-2"><ArrowRight size={16} className="text-blue-500"/> 성과급 구간(Incentive Threshold) 도달 여부</div>
        <div className="flex items-center gap-2"><ArrowRight size={16} className="text-blue-500"/> 팀 내 경쟁 강도와 Burnout</div>
      </div>
    </div>
  </div>
);

// Fixed Slide 3: Accurate Bar Chart scaling
const Slide3_Overview = () => {
  const chartData = [
    {label: '3M', val: 12},
    {label: '6M', val: 28}, // Spike
    {label: '9M', val: 15},
    {label: '1Y', val: 10},
    {label: '1.5Y', val: 18}, // 2nd Spike
    {label: '2Y', val: 8},
    {label: '3Y', val: 5},
  ];
  
  // Find max value to normalize bar heights
  const maxVal = Math.max(...chartData.map(d => d.val));

  return (
    <div className="h-full px-8 py-4">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
        <BarChart2 className="text-blue-500" />
        이탈 현황 오버뷰 (Overview)
      </h2>
      <div className="grid grid-cols-3 gap-6 h-[80%]">
        {/* KPI Cards */}
        <div className="col-span-1 space-y-6">
          <Card className="text-center py-8">
            <div className="text-slate-400 text-sm mb-2">3년 이하 총 이탈률</div>
            <div className="text-5xl font-black text-red-500 mb-2">28.4%</div>
            <div className="text-xs text-red-400 flex justify-center items-center gap-1">
              <TrendingUp size={12} /> 전년 대비 +4.2%p 증가
            </div>
          </Card>
          <Card className="text-center py-8">
            <div className="text-slate-400 text-sm mb-2">평균 이탈 시점</div>
            <div className="text-5xl font-black text-orange-400 mb-2">8.5<span className="text-2xl font-normal text-slate-500">개월</span></div>
            <div className="text-xs text-slate-400">Onboarding 직후 급증</div>
          </Card>
          <Card className="text-center py-8">
            <div className="text-slate-400 text-sm mb-2">이탈자 평균 성과달성률</div>
            <div className="text-5xl font-black text-blue-400 mb-2">92%</div>
            <div className="text-xs text-slate-400">생각보다 고성과자 이탈 비중 높음</div>
          </Card>
        </div>

        {/* Main Trend Chart */}
        <div className="col-span-2">
          <Card className="h-full flex flex-col">
            <h3 className="text-lg font-bold text-slate-300 mb-4">근속 기간별 이탈 생존 분석 (Survival Analysis)</h3>
            <div className="flex-1 flex items-end gap-2 px-4 pb-4 relative border-b border-l border-slate-600">
               {/* Fixed Bar Chart Visualization with proper scaling */}
               {chartData.map((d, i) => {
                 // Calculate height percentage relative to max value (leaving 10% headroom)
                 const heightPct = (d.val / maxVal) * 90;
                 return (
                   <div key={i} className="flex-1 flex flex-col justify-end group h-full">
                     <div className="flex flex-col justify-end h-full relative">
                        {/* Tooltip on hover */}
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-max opacity-0 group-hover:opacity-100 transition-opacity z-10">
                          <span className="text-xs font-bold text-white bg-slate-700 px-2 py-1 rounded shadow-lg">{d.val}%</span>
                        </div>
                        
                        {/* Bar */}
                        <div 
                          style={{height: `${heightPct}%`}} 
                          className={`w-full rounded-t-lg transition-all duration-500 relative ${d.val > 20 ? 'bg-gradient-to-t from-red-600 to-red-400' : 'bg-gradient-to-t from-blue-600 to-blue-400'}`}
                        >
                            {/* Bar Label */}
                           {d.val > 10 && <span className="absolute top-2 w-full text-center text-[10px] font-bold text-white/80">{d.val}%</span>}
                           
                           {/* Specific Annotation for Death Valley (6M) - Adjusted position lower (mb-4 -> mb-1) */}
                           {d.label === '6M' && (
                             <div className="absolute bottom-full left-[60%] mb-1 z-20 w-max animate-bounce-slight">
                               <div className="bg-slate-800/90 p-2 rounded border border-red-500/50 text-xs text-red-300 backdrop-blur shadow-lg text-center relative">
                                 {/* Adjusted arrow position to point correctly */}
                                 <div className="absolute -bottom-1 left-2 w-2 h-2 bg-slate-800 border-r border-b border-red-500/50 rotate-45"></div>
                                 🚩 Death Valley<br/>(입사 6개월 차)
                               </div>
                             </div>
                           )}

                           {/* Specific Annotation for Promotion Gap (1.5Y) - Adjusted position lower (mb-4 -> mb-1) */}
                           {d.label === '1.5Y' && (
                             <div className="absolute bottom-full left-[60%] mb-1 z-20 w-max">
                               <div className="bg-slate-800/90 p-2 rounded border border-orange-500/50 text-xs text-orange-300 backdrop-blur shadow-lg relative">
                                 <div className="absolute -bottom-1 left-4 w-2 h-2 bg-slate-800 border-r border-b border-orange-500/50 rotate-45"></div>
                                 ⚠️ Promotion Gap<br/>(1.5년 차)
                               </div>
                             </div>
                           )}
                        </div>
                     </div>
                     <div className="text-center text-xs text-slate-400 mt-2 font-medium">{d.label}</div>
                   </div>
                 );
               })}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

const Slide4_DeepAnalysis1 = () => (
  <div className="h-full px-8 py-4">
    <div className="flex justify-between items-end mb-6">
      <h2 className="text-2xl font-bold text-white flex items-center gap-3">
        <Activity className="text-blue-500" />
        심층 분석 1: 성과와 이탈의 '죽음의 계곡'
      </h2>
      {/* Data Source tag removed */}
    </div>

    <div className="grid grid-cols-2 gap-8 h-[80%]">
      {/* Heatmap Section */}
      <Card className="flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-slate-200">성과 등급별/기간별 이탈 위험 히트맵</h3>
          <div className="flex gap-2">
            <span className="w-2 h-2 rounded-full bg-red-600"></span><span className="text-xs text-slate-400">High Risk</span>
          </div>
        </div>
        <div className="flex-1 flex items-center">
          <Heatmap />
        </div>
        <div className="mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
          <p className="text-sm text-red-200 font-bold">💡 Key Insight</p>
          <p className="text-xs text-red-100 mt-1">
            입사 4-6개월 차 <b>D등급(저성과)</b> 직원의 이탈뿐만 아니라, <br/>
            <b>A등급(고성과)</b> 직원의 1년 전후 이탈률도 30%로 매우 높음.
          </p>
        </div>
      </Card>

      {/* Bubble Chart Section */}
      <Card className="flex flex-col">
        <div className="mb-4">
          <h3 className="text-lg font-bold text-slate-200">성과 대비 인센티브 만족도 분포</h3>
          <p className="text-xs text-slate-400">High Performer가 왜 떠나는가?</p>
        </div>
        <div className="flex-1 flex items-center justify-center p-4">
          <BubbleChart />
        </div>
        <div className="mt-4 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
          <p className="text-sm text-blue-200 font-bold">💡 Key Insight</p>
          <p className="text-xs text-blue-100 mt-1">
            우측 하단(High Performance, Low Satisfaction) 군집이 핵심 문제.<br/>
            초기 인센티브 캡(Cap) 정책이 고성과 신규 입사자의 동기 부여를 저해함.
          </p>
        </div>
      </Card>
    </div>
  </div>
);

const Slide5_DeepAnalysis2 = () => (
  <div className="h-full px-8 py-4">
    <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
      <Users className="text-blue-500" />
      심층 분석 2: 이탈자와 재직자의 DNA 차이
    </h2>

    <div className="grid grid-cols-12 gap-8 h-[80%]">
      {/* Left: Radar Chart */}
      <div className="col-span-5 flex flex-col justify-center">
        <Card className="h-full flex flex-col items-center justify-center">
          <h3 className="text-lg font-bold text-slate-200 mb-6 self-start w-full border-b border-slate-700 pb-2">역량 및 환경 만족도 비교</h3>
          <RadarChart 
            data={[
              { label: '목표 달성력', A: 85, B: 90 }, // Stay, Leave
              { label: '활동량(Call)', A: 80, B: 95 },
              { label: '관리자 코칭', A: 75, B: 40 },
              { label: '동료 관계', A: 85, B: 60 },
              { label: '직무 적합성', A: 70, B: 50 },
            ]} 
          />
          <div className="mt-6 text-center text-sm text-slate-400">
            * 이탈자(빨강)는 <b className="text-white">개인 활동량과 목표 달성력</b>은 높으나<br/>
            <b className="text-white">관리자 코칭</b>과 <b className="text-white">조직 유대감</b>이 현저히 낮음.
          </div>
        </Card>
      </div>

      {/* Right: Textual Analysis & Persona */}
      <div className="col-span-7 space-y-6">
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
          <h3 className="text-xl font-bold text-white mb-4">🔍 페르소나 분석: 누가 떠나는가?</h3>
          
          <div className="flex gap-4 mb-6">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center text-2xl">🔥</div>
            <div>
              <h4 className="font-bold text-lg text-orange-400">The Lone Wolf (고독한 늑대형)</h4>
              <p className="text-sm text-slate-300">
                입사 1년차. 개인 실적은 Top 10%에 들지만, 팀 미팅 참여도가 낮고 매니저와의 1:1 면담 횟수가 평균의 절반 수준. 
                "내가 번 만큼 못 가져간다"는 불만이 큼.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-slate-400 to-slate-600 flex items-center justify-center text-2xl">💧</div>
            <div>
              <h4 className="font-bold text-lg text-slate-400">The Early Burnout (조기 소진형)</h4>
              <p className="text-sm text-slate-300">
                입사 6개월차. 초반 3개월간 과도한 활동량(Call/Meeting)을 보였으나, 
                첫 Deal Closing이 4개월차로 지연되면서 급격히 동기 상실. 멘탈 케어 부재.
              </p>
            </div>
          </div>
        </div>

        <Card className="bg-gradient-to-r from-blue-900/30 to-slate-900/30">
          <h4 className="font-bold text-blue-400 mb-2">📊 Statistic Insight</h4>
          <ul className="space-y-2 text-sm text-slate-300">
            <li className="flex items-center gap-2">
              <span className="w-1 h-1 bg-white rounded-full"></span>
              주간 코칭 횟수 1회 미만인 직원의 이탈률: <b className="text-red-400">3.5배 높음</b>
            </li>
            <li className="flex items-center gap-2">
              <span className="w-1 h-1 bg-white rounded-full"></span>
              입사 첫 달 목표 120% 초과 달성자의 1년 내 이탈률: <b className="text-orange-400">40% (Burnout)</b>
            </li>
          </ul>
        </Card>
      </div>
    </div>
  </div>
);

const Slide6_Conclusion = () => (
  <div className="h-full px-8 py-4">
    <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
      <Briefcase className="text-blue-500" />
      종합 결론 및 해결 방안 (Action Plan)
    </h2>

    <div className="grid grid-cols-3 gap-6 h-[80%]">
      {/* Conclusion Summary */}
      <Card className="col-span-1 border-l-4 border-l-red-500">
        <h3 className="text-xl font-bold text-white mb-4">종합 진단</h3>
        <p className="text-slate-300 leading-relaxed mb-4">
          Sales 저년차 이탈의 핵심 원인은<br/>
          단순한 '성과 부진'이 아니라,
        </p>
        <div className="space-y-4">
          <div className="bg-slate-900 p-4 rounded-lg border border-slate-700">
            <div className="text-red-400 font-bold mb-1">1. 성과-보상의 Time Lag</div>
            <p className="text-xs text-slate-400">성과는 즉각 나오지만 인센티브 지급 주기(분기/반기)가 길어 동기 부여 저하</p>
          </div>
          <div className="bg-slate-900 p-4 rounded-lg border border-slate-700">
            <div className="text-orange-400 font-bold mb-1">2. 고립된 성장 환경</div>
            <p className="text-xs text-slate-400">Manager의 코칭 없이 '개인기'에 의존하는 구조가 고립감 심화</p>
          </div>
        </div>
      </Card>

      {/* Solutions */}
      <div className="col-span-2 space-y-4">
        <h3 className="text-xl font-bold text-white mb-2">전략적 해결 방안 (Retention Strategy)</h3>
        
        {/* Solution 1 */}
        <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 flex items-center gap-4 hover:border-blue-500 transition-colors cursor-pointer group">
          <div className="p-4 bg-blue-500/20 rounded-full text-blue-400 group-hover:scale-110 transition-transform">
            <DollarSign size={24} />
          </div>
          <div className="flex-1">
            <h4 className="font-bold text-blue-400 text-lg">Fast-Track Incentive 제도 도입</h4>
            <p className="text-slate-300 text-sm">신규 입사자 대상 첫 6개월간 인센티브 지급 주기를 '월 단위'로 단축하여 즉각적 보상 제공 (Spot Bonus)</p>
          </div>
        </div>

        {/* Solution 2 */}
        <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 flex items-center gap-4 hover:border-emerald-500 transition-colors cursor-pointer group">
          <div className="p-4 bg-emerald-500/20 rounded-full text-emerald-400 group-hover:scale-110 transition-transform">
            <Users size={24} />
          </div>
          <div className="flex-1">
            <h4 className="font-bold text-emerald-400 text-lg">Sales Enablement 코칭 의무화</h4>
            <p className="text-slate-300 text-sm">팀장 평가 항목에 '팀원 유지율(Retention)' 및 '주간 코칭 시간' 반영. 신규 입사자 전담 멘토링 프로그램(Buddy) 강화.</p>
          </div>
        </div>

        {/* Solution 3 */}
        <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 flex items-center gap-4 hover:border-purple-500 transition-colors cursor-pointer group">
          <div className="p-4 bg-purple-500/20 rounded-full text-purple-400 group-hover:scale-110 transition-transform">
            <Activity size={24} />
          </div>
          <div className="flex-1">
            <h4 className="font-bold text-purple-400 text-lg">Early Warning System 구축</h4>
            <p className="text-slate-300 text-sm">3개월 연속 활동량 대비 실적 저조자, 혹은 120% 초과 달성 후 급격한 활동 저하자 자동 식별 및 면담 진행.</p>
          </div>
        </div>

      </div>
    </div>
  </div>
);

// --- Main App Component ---

const App = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isGridView, setIsGridView] = useState(false);
  const slides = [
    Slide1_Title,
    Slide2_Hypothesis,
    Slide3_Overview,
    Slide4_DeepAnalysis1,
    Slide5_DeepAnalysis2,
    Slide6_Conclusion
  ];

  const nextSlide = () => setCurrentSlide(prev => Math.min(prev + 1, slides.length - 1));
  const prevSlide = () => setCurrentSlide(prev => Math.max(prev - 1, 0));

  const CurrentSlideComponent = slides[currentSlide];

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (isGridView) return; // Disable keyboard nav in grid view
      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isGridView, currentSlide]); // Dependency update for correct state

  return (
    <div className="flex flex-col h-screen w-full bg-slate-900 text-slate-200 overflow-hidden font-sans selection:bg-blue-500 selection:text-white">
      {/* Top Bar / Progress */}
      <div className="h-1 bg-slate-800 w-full flex-shrink-0">
        <div 
          className="h-full bg-blue-500 transition-all duration-500 ease-out" 
          style={{ width: `${((currentSlide + 1) / slides.length) * 100}%` }}
        />
      </div>

      {/* Main Slide Area */}
      <main className={`flex-1 relative w-full max-w-7xl mx-auto p-4 md:p-8 flex flex-col ${isGridView ? 'overflow-y-auto' : 'overflow-hidden'}`}>
        {!isGridView ? (
            <>
                <div className="absolute top-4 right-8 text-slate-500 text-sm font-mono tracking-widest z-10">
                  SLIDE {currentSlide + 1} / {slides.length}
                </div>

                <div className="flex-1 bg-slate-900/50 rounded-2xl shadow-2xl overflow-hidden border border-slate-800 relative">
                  <CurrentSlideComponent />
                </div>
            </>
        ) : (
            <div className="space-y-8 pb-8">
                {slides.map((SlideComponent, index) => (
                    <div key={index} className="flex flex-col gap-2">
                        <div className="text-slate-500 text-sm font-mono font-bold pl-2">SLIDE {index + 1}</div>
                        <div className="h-[600px] bg-slate-900/50 rounded-2xl shadow-2xl overflow-hidden border border-slate-800 relative">
                             <SlideComponent />
                        </div>
                    </div>
                ))}
            </div>
        )}
      </main>

      {/* Navigation Bar */}
      <footer className="h-20 flex-shrink-0 border-t border-slate-800 bg-slate-900/80 backdrop-blur flex items-center justify-between px-8">
        <div className="flex items-center gap-4 text-slate-400">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-bold text-white">S</div>
          <span className="font-semibold text-sm hidden md:block">Sales Retention Analytics Report</span>
        </div>
        
        <div className="flex items-center gap-4">
            <Button 
                onClick={() => setIsGridView(!isGridView)} 
                variant="outline" 
                className="mr-4"
                title="모아보기 / 인쇄 모드"
            >
                {isGridView ? <Monitor size={20} /> : <Grid size={20} />}
                {isGridView ? 'Slide View' : 'Grid / Print View'}
            </Button>

          {!isGridView && (
            <>
                <Button onClick={prevSlide} variant="secondary" className={currentSlide === 0 ? 'opacity-50 cursor-not-allowed' : ''}>
                    <ChevronLeft size={20} /> Prev
                </Button>
                <div className="flex gap-1">
                    {slides.map((_, idx) => (
                    <div 
                        key={idx} 
                        onClick={() => setCurrentSlide(idx)}
                        className={`w-2 h-2 rounded-full cursor-pointer transition-all ${idx === currentSlide ? 'bg-blue-500 w-6' : 'bg-slate-700 hover:bg-slate-600'}`}
                    />
                    ))}
                </div>
                <Button onClick={nextSlide} variant="primary" className={currentSlide === slides.length - 1 ? 'opacity-50 cursor-not-allowed' : ''}>
                    Next <ChevronRight size={20} />
                </Button>
            </>
          )}
        </div>
      </footer>
    </div>
  );
};

export default App;
