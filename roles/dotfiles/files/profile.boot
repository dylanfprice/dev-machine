; vi: ft=clojure

(require 'boot.repl)

(swap! boot.repl/*default-dependencies*
       concat '[[cider/cider-nrepl "0.14.0"] 
                [jonase/eastwood "0.2.3"]])

(swap! boot.repl/*default-middleware*
       conj 'cider.nrepl/cider-middleware)
