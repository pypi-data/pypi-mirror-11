(define-syntax apply*
    (syntax-rules ()
        ((apply* func args ... ((name value) ...))
            (apply func (list args ...) (dict (zip (list name ...) (list value ...)))))))

