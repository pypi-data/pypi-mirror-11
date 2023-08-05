## Depends:

`python`: 2.7

`qiniu`: 6.1.6|6.x

`node`: v0.12.5

`npm`: 2.11.2

`gitbook`: 2.2.0


## Install


---

Install command:
```
pip install docbook
```

## docbook.conf

---

When you install complete,you should modify the config file: docbook.conf. for example:
```
[qiniu]
bucket_name = test-qn
ACCESS_KEY = ymtUGLMUVsngMcRRZCqnt_m9lOZ5d8pZ1T_KPhA
SECRET_KEY = toOvcxKuL7LcvQdfF646EKGX8Ak4UAR-f3scYMJ

[docbook]
prefix_path = 
input_dir = 
format = site
```

## docbook

---

Use to generate docment and upload to qiniu to read online. for example:

```
#docbook
```
- `input_dir` is current directory
- `output_dir` in /tmp/xxx,this directory will be auto delete when the jobs complete.
- `format` is 'site'
- `prefix_path` is null


```
#docbook -o /tmp/xxx
```
- `input_dir` is current directory
- `output_dir` is /tmp/xxx
- `format` is site
- `prefix_path` is null

```
#docbook -i input_dir -o /tmp/xxx -p aa
```
- `input_dir` is input_dir
- `output_dir` is /tmp/xxx
- `format` is site
- `prefix_path` is aa

## docbook-manage

---

Use to batch list/delete files. for example:
```
#docbook-manage -b test-qn -a list
```
- list all files in test-qn

```
#docbook-manage -b test-qn -a list -p test
```
- list all start with 'test' files in test-qn

```
#docbook-manage -b test-qn -a delete -p test
```
- delete all startwith 'test' files

```
#docbook-manage -b test-qn -a delete -p ''
```
- delete all files in bucket named: test-qn
