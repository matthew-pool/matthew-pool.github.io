import { useState } from 'react';
import { ChevronRight, RotateCcw } from 'lucide-react';

const ExistenceParadox = () => {
  const [screen, setScreen] = useState('question');
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);

  const philosophicalArguments = [
    {
      num: 1,
      text: "The Infinite Past Problem: Some philosophers argue there cannot be an infinite past due to the \"infinite traversal problem\"—if an infinite amount of time preceded today, we could never have reached now. However, critics contend this misconstrues infinity: if the past is infinite, there's no starting point to traverse from; each moment simply has predecessors extending backward infinitely."
    },
    {
      num: 2,
      text: "The Creator Regress Problem: If the universe was created, what created the creator? This seems to lead to an infinite regress. However, classical theistic arguments propose an \"uncaused cause\" or \"necessary being\" that exists outside of time and space, not requiring its own creator. This remains philosophically contested."
    },
    {
      num: 3,
      text: "The Finite Beginning: If we accept both that infinite regress is impossible (Argument 1) and that an uncaused creator is problematic (Argument 2), then our cause-effect universe must have begun a finite time ago without a transcendent creator."
    },
    {
      num: 4,
      text: "The \"From Nothing\" Problem: Can something come from absolute nothing? Classical logic suggests nothing can emerge from nonexistence. However, quantum mechanics reveals spontaneous vacuum fluctuations, suggesting the rules may differ at fundamental levels. The concept of \"nothing\" itself may be incoherent in physics."
    },
    {
      num: 5,
      text: "The Singularity Hypothesis: Einstein's General Relativity predicts our universe began from a singularity—a state of extreme density and energy where our equations break down and time itself \"begins.\" This provides a mathematical framework but doesn't answer why the singularity existed or what \"caused\" it to expand."
    },
    {
      num: 6,
      text: "The Necessity of Existence: Perhaps \"absolute nothing\" is impossible—if something emerged from nothing, that \"nothing\" must have had some property or potential. This suggests existence in some form may be necessary. However, this still doesn't explain why this particular universe exists rather than some other configuration."
    },
    {
      num: 7,
      text: "Alternative Possibilities: Other frameworks exist: eternal cyclic universes (bouncing cosmologies), the universe itself as a necessary being, quantum multiverse theories where our universe is one of countless variations, or a timeless/eternal ground of being. Each has philosophical and scientific considerations."
    },
    {
      num: 8,
      text: "The Limits of Understanding: Our universe may be embedded in a larger reality with different laws. Whether the explanation involves a deity, quantum processes, mathematical necessity, consciousness, or something beyond our comprehension, we're constrained by the limits of human cognition and the physical laws we observe within our universe."
    },
    {
      num: 9,
      text: "Final Reflection: Every logical path—infinite past, created universe, spontaneous emergence, or necessary existence—encounters profound paradoxes or unanswered questions. This isn't a failure of logic but a reflection of the question's depth. We're asking about the preconditions for existence itself using minds and logic that exist within that very existence. Perhaps the question transcends our conceptual frameworks."
    }
  ];

  const handleSubmit = () => {
    if (selectedAnswer !== null) {
      setScreen('arguments');
    }
  };

  const handleReset = () => {
    setSelectedAnswer(null);
    setScreen('question');
  };

  const getExplanation = () => {
    if (selectedAnswer === 'created') {
      return {
        response: "You chose the creation hypothesis. This faces the challenge of infinite regress (what created the creator?), though some argue for a necessary being outside of time that requires no creator. This remains one of humanity's oldest philosophical debates.",
        insight: "Many theologians and philosophers argue that a timeless, necessary being (God) doesn't require a cause because it exists outside the causal chain of temporal events. This addresses the regress problem but raises questions about how something timeless can interact with time."
      };
    } else if (selectedAnswer === 'infinite') {
      return {
        response: "You chose an infinite past. This faces the infinite traversal problem (how did we reach today if infinite time preceded it?), though critics argue this misunderstands mathematical infinity. Some cosmological models like eternal inflation or cyclic universes explore this possibility.",
        insight: "The infinite traversal argument assumes infinity works like a very large finite number, but mathematicians note that in an actually infinite past, every moment would simply have a finite predecessor. Additionally, some quantum cosmology models suggest time itself may be emergent rather than fundamental."
      };
    } else {
      return {
        response: "You acknowledged the profound mystery. Both \"created\" and \"infinite past\" encounter deep philosophical paradoxes, yet alternatives like spontaneous quantum emergence or necessary existence raise their own puzzles. This question may transcend our current frameworks.",
        insight: "Physicist and philosophers increasingly recognize that the question \"why is there something rather than nothing?\" may not have an answer expressible in terms we understand. It touches the limits of science, philosophy, and human cognition itself."
      };
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white p-6 md:p-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-6xl font-bold text-center mb-6 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
          The Existence Paradox
        </h1>
        <p className="text-center text-gray-400 mb-12 text-lg">
          An exploration of why existence itself remains philosophy's deepest mystery
        </p>

        {screen === 'question' && (
          <div className="space-y-8 animate-fade-in">
            <h2 className="text-2xl md:text-4xl font-semibold text-center mb-12 leading-relaxed">
              Was this universe created, does it have an infinite past, or something else?
            </h2>

            <div className="space-y-4">
              <label className="flex items-center p-6 bg-gray-800/50 rounded-xl border-2 border-gray-700 hover:border-purple-500 transition-all cursor-pointer group">
                <input
                  type="radio"
                  name="answer"
                  value="created"
                  checked={selectedAnswer === 'created'}
                  onChange={(e) => setSelectedAnswer(e.target.value)}
                  className="w-6 h-6 text-purple-500 focus:ring-purple-500 focus:ring-2"
                />
                <span className="ml-4 text-xl md:text-2xl group-hover:text-purple-300 transition-colors">
                  Created by something/someone
                </span>
              </label>

              <label className="flex items-center p-6 bg-gray-800/50 rounded-xl border-2 border-gray-700 hover:border-blue-500 transition-all cursor-pointer group">
                <input
                  type="radio"
                  name="answer"
                  value="infinite"
                  checked={selectedAnswer === 'infinite'}
                  onChange={(e) => setSelectedAnswer(e.target.value)}
                  className="w-6 h-6 text-blue-500 focus:ring-blue-500 focus:ring-2"
                />
                <span className="ml-4 text-xl md:text-2xl group-hover:text-blue-300 transition-colors">
                  Infinite past (always existed)
                </span>
              </label>

              <label className="flex items-center p-6 bg-gray-800/50 rounded-xl border-2 border-gray-700 hover:border-pink-500 transition-all cursor-pointer group">
                <input
                  type="radio"
                  name="answer"
                  value="mystery"
                  checked={selectedAnswer === 'mystery'}
                  onChange={(e) => setSelectedAnswer(e.target.value)}
                  className="w-6 h-6 text-pink-500 focus:ring-pink-500 focus:ring-2"
                />
                <span className="ml-4 text-xl md:text-2xl group-hover:text-pink-300 transition-colors">
                  The answer remains unknown
                </span>
              </label>
            </div>

            <div className="flex justify-center mt-12">
              <button
                onClick={handleSubmit}
                disabled={selectedAnswer === null}
                className="px-12 py-4 text-xl md:text-2xl font-semibold bg-gradient-to-r from-purple-600 to-pink-600 rounded-full hover:from-purple-500 hover:to-pink-500 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed transition-all flex items-center gap-3 shadow-lg hover:shadow-purple-500/50"
              >
                Explore
                <ChevronRight className="w-6 h-6" />
              </button>
            </div>
          </div>
        )}

        {screen === 'arguments' && (
          <div className="space-y-8 animate-fade-in">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-purple-300">
              Philosophical Arguments
            </h2>
            <p className="text-center text-gray-400 mb-8 max-w-2xl mx-auto">
              These are contested philosophical positions, not proven facts. Each encounters deep paradoxes.
            </p>

            <div className="space-y-6">
              {philosophicalArguments.map((argument) => (
                <div
                  key={argument.num}
                  className="p-6 bg-gray-800/50 rounded-xl border-l-4 border-purple-500 hover:bg-gray-800/70 transition-all"
                >
                  <div className="flex items-start gap-4">
                    <span className="text-3xl font-bold text-purple-400 flex-shrink-0">
                      {argument.num}
                    </span>
                    <p className="text-lg md:text-xl leading-relaxed text-gray-200">
                      {argument.text}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-center mt-12">
              <button
                onClick={() => {
                  setScreen('results');
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="px-12 py-4 text-xl md:text-2xl font-semibold bg-gradient-to-r from-blue-600 to-purple-600 rounded-full hover:from-blue-500 hover:to-purple-500 transition-all flex items-center gap-3 shadow-lg hover:shadow-blue-500/50"
              >
                See Results
                <ChevronRight className="w-6 h-6" />
              </button>
            </div>
          </div>
        )}

        {screen === 'results' && (
          <div className="space-y-8 animate-fade-in">
            <div className="mb-12 text-center">
              <div className="text-6xl md:text-7xl font-black mb-6 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
                Your Position
              </div>
            </div>

            <div className="space-y-6 max-w-3xl mx-auto">
              <div className="p-8 bg-gray-800/50 rounded-xl border-2 border-purple-500/50">
                <p className="text-xl md:text-2xl text-gray-200 leading-relaxed mb-6">
                  You chose: <span className="font-bold text-purple-300">
                    {selectedAnswer === 'created' ? 'Created by something/someone' : 
                     selectedAnswer === 'infinite' ? 'Infinite past' : 
                     'The answer remains unknown'}
                  </span>
                </p>
                
                <div className="p-6 bg-blue-900/30 rounded-lg border-l-4 border-blue-400 mb-6">
                  <h3 className="text-xl font-bold text-blue-300 mb-3">What This Means:</h3>
                  <p className="text-lg md:text-xl text-gray-200 leading-relaxed">
                    {getExplanation().response}
                  </p>
                </div>

                <div className="p-6 bg-purple-900/30 rounded-lg border-l-4 border-purple-400">
                  <h3 className="text-xl font-bold text-purple-300 mb-3">Deeper Insight:</h3>
                  <p className="text-lg md:text-xl text-gray-200 leading-relaxed">
                    {getExplanation().insight}
                  </p>
                </div>
              </div>

              <div className="p-8 bg-gradient-to-r from-purple-900/40 to-pink-900/40 rounded-xl border-2 border-purple-500/50">
                <h3 className="text-2xl font-bold text-center mb-4 text-purple-200">The Paradox Remains</h3>
                <p className="text-lg md:text-xl text-gray-200 leading-relaxed text-center">
                  Whether through divine creation, eternal existence, quantum fluctuation, mathematical necessity, or something beyond our understanding—every explanation encounters profound mysteries. This isn't a defect in our reasoning but may reflect the question's fundamental nature: we're asking about the preconditions for existence using minds that exist within existence itself.
                </p>
              </div>
            </div>

            <button
              onClick={handleReset}
              className="px-12 py-4 text-xl md:text-2xl font-semibold bg-gradient-to-r from-purple-600 to-pink-600 rounded-full hover:from-purple-500 hover:to-pink-500 transition-all flex items-center gap-3 mx-auto shadow-lg hover:shadow-purple-500/50"
            >
              <RotateCcw className="w-6 h-6" />
              Explore Again
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExistenceParadox;