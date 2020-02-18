; vi: ft=clojure

(set-env! :dependencies '[[nrepl "0.6.0"]
                          [cider/cider-nrepl "0.24.0"]])

(require '[cider.tasks :refer [add-middleware]])

(task-options! add-middleware {:middleware '[cider.nrepl.middleware.apropos/wrap-apropos
                                             cider.nrepl.middleware.version/wrap-version]})

