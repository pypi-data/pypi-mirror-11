# Kubetemplate

Kubernetes specific helpers and Jinja templating

Usage `kubet [-h] [-i INPUT_T] [-o OUTPUT_T]`  
`-h` help  
`-i` input target path, defaults to targets in .kubetemplate file  
`-o` output target path if input target path specified, defaults to same directory

Put a `.kubetemplate` file in your project root. It looks like this:
```yaml
compiler:
  targets:
    - path: app
      to: app.compiled
    - path: files
  output_prefix: 'pan.'
```

This can be used, for example, to [https://github.com/hasura/kubetemplate/tree/master/example](generate a Kubernetes secret that contains Google service account credentials).
