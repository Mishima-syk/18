# dashで可視化

## requirements
- rdkit
- scikit-learn
- pandas
- dash
- dash-bootstrap-components
- dash_dangerously_set_inner_html

## prepare env

```bash
$ conda env create -n dashapp python=3.8
$ conda activate dashapp
$ conda install -c conda-forge rdkit, dash, dash-bootstrap-compnents, scikit-learn, pandas
$ pip install dash-dangerously-set-inner-html
```