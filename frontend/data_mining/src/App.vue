<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(false)
const result = ref(null)
const error = ref(null)
const isVisible = ref(false)

onMounted(() => {
   setTimeout(() => isVisible.value = true, 100)
})

// Scenario Definition (Raw ANOVA Features)
const form = reactive({
  product_related: 15,          
  product_related_duration: 600,
  page_values: 10,              
  exit_rates: 0.05,            
  month: 'Nov',
  is_special_day: false,
  is_returning_visitor: true
})

const availableMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const simulate = async () => {
  loading.value = true
  result.value = null
  error.value = null
  try {
    const res = await axios.post('http://localhost:8000/predict', form)
    if (res.data.error) throw new Error(res.data.error)
    setTimeout(() => {
        result.value = res.data
        loading.value = false
    }, 800)
  } catch (e) {
    console.error(e)
    error.value = e.message || "Connection Failed. Check Backend."
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen font-sans flex flex-col relative overflow-hidden bg-slate-50 text-slate-800">
    
    <!-- Background Image & Overlay -->
    <div class="fixed inset-0 bg-cover bg-center bg-no-repeat z-0" style="background-image: url('/background1.jpg');"></div>
    <div class="fixed inset-0 bg-white/20 backdrop-blur-[2px] z-0"></div> 
    <div class="fixed inset-0 bg-gradient-to-br from-indigo-100/40 via-white/20 to-fuchsia-100/40 mix-blend-overlay z-0"></div>

    <!-- Floating Orbs -->
    <div class="fixed top-20 left-20 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-pulse-slow mix-blend-multiply z-0"></div>
    <div class="fixed bottom-20 right-20 w-80 h-80 bg-cyan-400/20 rounded-full blur-3xl animate-pulse-slow mix-blend-multiply z-0" style="animation-delay: 2s;"></div>

    <!-- HEADER (Fixed Top) -->
    <header class="relative z-50 bg-slate-200 border-b border-slate-300 py-2 px-8 shadow-sm flex items-center justify-between">
       <div class="flex items-center gap-3">
          <img src="/Logo2.png" alt="Logo" class="h-14 w-auto object-contain drop-shadow-md" />
          <div>
            <h1 class="text-xl font-black text-slate-800 tracking-tight leading-none">Online Shopper Prediction</h1>
            <p class="text-[10px] uppercase font-bold text-slate-500 tracking-widest mt-0.5">Real-time Analysis System</p>
          </div>
       </div>
    </header>

    <!-- Main Content (Grow) -->
    <main class="relative z-10 flex-grow flex items-center justify-center p-4 md:p-8 overflow-y-auto w-full">
         <div class="max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-center" 
         :class="{ 'opacity-0 translate-y-8': !isVisible, 'opacity-100 translate-y-0': isVisible }"
         style="transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);">

      <!-- LEFT: CONFIGURATION PANEL -->
      <div class="lg:col-span-5 space-y-6">

         <!-- Glass Card -->
         <div class="glass-card rounded-3xl p-6 space-y-6 animate-fade-in-delay shadow-xl shadow-indigo-100/50">
            
            <h3 class="text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">Key Drivers (ANOVA)</h3>

            <!-- SLIDER: ProductRelated -->
            <div class="relative group">
               <div class="flex justify-between items-end mb-2">
                  <label class="font-bold text-slate-700 text-sm flex items-center gap-2">
                      Product Pages
                  </label>
                  <span class="font-black font-mono text-indigo-600">{{ form.product_related }}</span>
               </div>
               <input type="range" class="custom-slider w-full bg-indigo-200"
                      min="0" max="100" v-model.number="form.product_related">
            </div>

            <!-- SLIDER: Duration -->
            <div class="relative group">
               <div class="flex justify-between items-end mb-2">
                  <label class="font-bold text-slate-700 text-sm flex items-center gap-2">
                      Duration (sec)
                  </label>
                  <span class="font-black font-mono text-indigo-600">{{ form.product_related_duration }}s</span>
               </div>
               <input type="range" class="custom-slider w-full bg-indigo-200"
                      min="0" max="5000" step="10" v-model.number="form.product_related_duration">
            </div>

            <!-- SLIDER: PageValues -->
            <div class="relative group">
               <div class="flex justify-between items-end mb-2">
                  <label class="font-bold text-slate-700 text-sm flex items-center gap-2">
                      Page Values
                  </label>
                  <span class="font-black font-mono text-emerald-600">{{ form.page_values }}</span>
               </div>
               <input type="range" class="custom-slider w-full bg-emerald-200"
                      min="0" max="150" step="0.1" v-model.number="form.page_values">
            </div>

            <!-- SLIDER: ExitRates -->
            <div class="relative group">
               <div class="flex justify-between items-end mb-2">
                  <label class="font-bold text-slate-700 text-sm flex items-center gap-2">
                      Exit Rate
                  </label>
                  <span class="font-black font-mono text-rose-600">{{ (form.exit_rates * 100).toFixed(0) }}%</span>
               </div>
               <input type="range" class="custom-slider w-full bg-rose-200"
                      min="0" max="1.0" step="0.01" v-model.number="form.exit_rates">
            </div>

            <div class="h-px bg-slate-200/60 my-4"></div>

            <!-- TOGGLES -->
            <div class="grid grid-cols-2 gap-4">
               <!-- Toggle 1: Returning Visitor -->
               <div class="bg-white/40 p-3 rounded-xl border border-white/50 flex flex-col gap-2 hover:bg-white/60 transition-colors cursor-pointer" @click="form.is_returning_visitor = !form.is_returning_visitor">
                  <div class="flex justify-between items-start">
                     <span class="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Visitor Type</span>
                     <div class="w-8 h-4 rounded-full relative transition-colors duration-300" 
                          :class="form.is_returning_visitor ? 'bg-indigo-500' : 'bg-slate-300'">
                        <div class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full transition-transform duration-300 shadow-sm"
                             :class="form.is_returning_visitor ? 'translate-x-4' : 'translate-x-0'"></div>
                     </div>
                  </div>
                  <span class="font-bold text-slate-700 text-xs">{{ form.is_returning_visitor ? 'Returning' : 'New Visitor' }}</span>
               </div>

               <!-- Toggle 2: Special Day -->
               <div class="bg-white/40 p-3 rounded-xl border border-white/50 flex flex-col gap-2 hover:bg-white/60 transition-colors cursor-pointer" @click="form.is_special_day = !form.is_special_day">
                  <div class="flex justify-between items-start">
                     <span class="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Event</span>
                     <div class="w-8 h-4 rounded-full relative transition-colors duration-300" 
                          :class="form.is_special_day ? 'bg-rose-500' : 'bg-slate-300'">
                        <div class="absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full transition-transform duration-300 shadow-sm"
                             :class="form.is_special_day ? 'translate-x-4' : 'translate-x-0'"></div>
                     </div>
                  </div>
                   <span class="font-bold text-slate-700 text-xs">{{ form.is_special_day ? 'Special Day' : 'Regular' }}</span>
               </div>
            </div>

            <!-- MONTH GRID -->
            <div>
               <label class="block font-bold text-slate-700 text-xs uppercase tracking-wider mb-2">Month</label>
               <div class="flex flex-wrap gap-1.5">
                  <button v-for="m in availableMonths" :key="m" @click="form.month = m"
                          :class="form.month === m 
                            ? 'bg-slate-800 text-white shadow-lg scale-105' 
                            : 'bg-white/50 text-slate-500 hover:bg-white hover:text-indigo-600'"
                          class="px-2.5 py-1 rounded-md text-[10px] font-bold border border-transparent transition-all duration-200">
                     {{ m }}
                  </button>
               </div>
            </div>

         </div>

         <!-- ACTION BUTTON -->
         <button @click="simulate" :disabled="loading"
                 class="w-full py-4 rounded-2xl text-white font-bold text-lg relative overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed animate-fade-in-delay-2 shadow-xl shadow-slate-900/20 transition-transform active:scale-95">
            <div class="absolute inset-0 bg-slate-900"></div>
            <div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
            <span class="relative z-10 flex items-center justify-center gap-2">
               <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
               <span v-else>Predict Outcome</span>
            </span>
         </button>

      </div>

      <!-- RIGHT: INSIGHT CARD -->
      <div class="lg:col-span-7">

         <!-- Empty State -->
         <div v-if="!result" class="w-full glass-card rounded-[2rem] flex flex-col items-center justify-center p-12 text-center group min-h-[500px]">
            <img src="/Logo2.png" alt="Logo" class="w-24 h-24 object-contain drop-shadow-xl mb-6 group-hover:scale-110 transition-transform duration-500" />
            <h3 class="text-2xl font-bold text-slate-800 mb-2">Online Shopper Prediction</h3>
            <p class="text-slate-500 max-w-xs mx-auto">Configure the ANOVA features to generate purchase probability.</p>
         </div>

         <!-- Result Card -->
         <div v-else class="w-full glass-card rounded-[2rem] overflow-hidden animate-up relative shadow-2xl shadow-indigo-200/40">
            
            <div class="h-2 w-full" :class="{
                  'bg-emerald-500': result.segment_color === 'green',
                  'bg-amber-500': result.segment_color === 'yellow',
                  'bg-slate-400': result.segment_color === 'gray'
            }"></div>

            <div class="p-8 md:p-10">
               <!-- Header -->
               <div class="flex justify-between items-start mb-8">
                  <div>
                  <h2 class="text-4xl font-black text-slate-800 leading-tight">{{ result.segment }}</h2>
                  </div>
                  <div class="text-right">
                     <span class="block text-6xl font-black tracking-tighter" :class="{
                        'text-emerald-500': result.segment_color === 'green',
                        'text-amber-500': result.segment_color === 'yellow',
                        'text-slate-400': result.segment_color === 'gray'
                     }">
                        {{ result.probability_percent }}%
                     </span>
                     <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Purchase Probability</span>
                  </div>
               </div>

               <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <!-- Recommendation -->
                  <div class="space-y-6">
                     <div class="bg-white/60 p-5 rounded-2xl border border-white/60 shadow-sm">
                        <h3 class="text-indigo-900/50 text-[10px] font-bold uppercase tracking-widest mb-2 flex items-center gap-2">
                            Action
                        </h3>
                        <p class="text-lg font-bold text-slate-800 leading-snug">
                           {{ result.recommended_action }}
                        </p>
                     </div>

                     <!-- Mini Metrics -->
                     <div class="flex gap-4">
                        <div class="flex-1 p-4 rounded-2xl bg-indigo-50/50 border border-indigo-100">
                           <div class="text-indigo-400 text-[10px] font-bold uppercase mb-1">Score</div>
                           <div class="text-2xl font-black text-slate-700">{{ result.analysis_drivers.interest }}</div>
                        </div>
                        <div class="flex-1 p-4 rounded-2xl bg-purple-50/50 border border-purple-100">
                           <div class="text-purple-400 text-[10px] font-bold uppercase mb-1">Risk Index</div>
                           <div class="text-2xl font-black text-slate-700">{{ result.analysis_drivers.risk }}</div>
                        </div>
                     </div>
                  </div>

                  <!-- Drivers -->
                  <div class="bg-slate-50/80 rounded-2xl p-6 border border-slate-100 space-y-4">
                     <h4 class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Model Drivers</h4>
                     
                     <div v-for="(val, key) in result.analysis_drivers" :key="key">
                        <div class="flex justify-between text-xs mb-1.5 font-bold text-slate-600 capitalize">
                           <span>{{ key }}</span>
                           <span>{{ val }}</span>
                        </div>
                        <div class="h-2 bg-slate-200 rounded-full overflow-hidden">
                           <div class="h-full rounded-full transition-all duration-1000"
                                :class="{
                                   'bg-indigo-500': key === 'interest',
                                   'bg-rose-500': key === 'risk',
                                   'bg-emerald-500': key === 'value_score'
                                }"
                                :style="`width: ${Math.min(100, val)}%`"></div>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
         </div>

         <!-- Error Toast -->
         <div v-if="error" class="fixed bottom-6 right-6 p-4 bg-white border border-red-100 shadow-xl rounded-xl animate-shake flex items-center gap-3 text-red-600 text-sm font-bold z-50">
            <span>⚠️</span> {{ error }}
         </div>

      </div>

    </div>
    </main>

    <!-- FOOTER (Fixed Bottom) -->
    <footer class="relative z-50 bg-slate-200 border-t border-slate-300 py-3 text-center">
       <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">
         © 2026 Online Shopper Prediction System. All Rights Reserved.
       </p>
    </footer>

  </div>
</template>

<style>
/* Glass Card Theme - Light */
.glass-card {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

/* Custom Slider */
.custom-slider {
  -webkit-appearance: none;
  appearance: none;
  height: 6px;
  border-radius: 999px;
  cursor: pointer;
}
.custom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15), 0 0 0 1px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}
.custom-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

/* Animations */
.animate-up { animation: popUp 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes popUp {
   from { opacity: 0; transform: translateY(20px) scale(0.98); }
   to { opacity: 1; transform: translateY(0) scale(1); }
}

.animate-fade-in { animation: fadeIn 0.8s ease-out; }
.animate-fade-in-delay { animation: fadeIn 0.8s ease-out 0.15s both; }
.animate-fade-in-delay-2 { animation: fadeIn 0.8s ease-out 0.3s both; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-pulse-slow { animation: pulse 6s infinite ease-in-out; }
.animate-gradient-x { background-size: 200%; animation: grad 3s infinite alternate; }
@keyframes grad { 0% { background-position: 0%; } 100% { background-position: 100%; } }
</style>
