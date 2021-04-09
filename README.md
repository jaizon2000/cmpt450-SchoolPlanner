# README.md

###### 🔗 Useful links

[Dash Callbacks](https://dash.plotly.com/basic-callbacks#dash-app-state) 

[Filtering Data Tables](https://dash.plotly.com/datatable/callbacks) 

###### 📑 Documentation Links

[Plotly Dash](https://dash.plotly.com/) 

[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/) 

[Pandas](http://pandas.pydata.org/docs/user_guide/10min.html) 

# Pandas and Database

[Counting rows](https://bit.ly/31YKV8e) 

# Student

A Class that represents a student.
Contains the data frame of Student’s courses

```python
# main.py

# Get data
df = pd.read_csv('cmpt-courses-cleaned.csv')
df_dict = df.to_dict('records')

stud = Student()
stud_df = df.copy().iloc[0:0]  # erase all rows but keep cols: https://bit.ly/2PCF5Xi

course_classes_list = [Course(c['id'], c['name'], c['credit'], c['description'], c['prereq']) for c in df_dict]
```

## Inputs Column
### Search courses

#### Output

`collapse-card-{i}` on its `style` 

`courses-results-container` - 

#### Input

`course-search-input` - 

#### State

### Card Toggles

#### Output

`collapse-#` - collapse tab

#### Input

`group=#-toggle` - card group toggle

`*args*` Having an [unknown number of arguments](https://bit.ly/3syoB0Z), [link 2](https://bit.ly/3fr7Kt9)

#### State

`collapse-#` - collapse tab

------

### Dropdown Multiselect

#### Output

`table` - student’s table

#### Input

`courses-input` - multiselect dropdown

#### State

**[States](https://bit.ly/3uePXK9) allow user to input before running the main action**

So instead of getting the input as soon as there’s a change, the input is only gotten when the `Input` is triggered.

`status-radio` - status of selected courses

`add-to-planner-btn` - button to add to table

- The `Inputs` in `@app.callback` 
  - the action function parameters (function below below `@app.callback`) are in the order of the input in `@app.callback`.

## Data Table

- [x] Export current data table
- [x] Import a data table (csv, json)
- [ ] reset button (delete all rows)
- [ ] how to modal

when importing, it take the string but it’s has, `“....”()” ”` so the double quote inside the double quote cause an error when splitting and is illegal.

[Stack overflow convo](https://bit.ly/39UCQWJ), [`quotechar`](https://bit.ly/3s478w9) 

### How to Import Modal

`import-modal`

`open-import` , `close-import`

The supported files you can export is `.csv` and `.xls.`

You ***must*** follow this column format (this means column name is case sensitive )

The only required cell to input is `Course ID`

| Course ID | Course Name | Credits | Prerequisites | Status |
| --------- | ----------- | ------- | ------------- | ------ |
| CMPT 103  | --          | --      | --            | --     |

### Importing

[Uploading Data](https://bit.ly/3mq82SK) 

#### Output

`my-table`

#### Input

`upload-table` - the upload container

`import-btn` 

### Data table

data table changes -> change checklist

#### Output

`check-list-input-X, value` 

#### Input

`my-table`

#### State

## Checklist Column

### Choosing a stream

`major-stream-input` - dropdown

`major-stream-checklist` - checklist stream container

`general-stream`

`game-stream`

`sys-info-stream` 

`database-stream`

[Dash Bootstrap Checklist Input](https://bit.ly/3sDJ8Bk) 

### change in checklist -> change data table

[Getting labels and values of checklist](https://community.plotly.com/t/dcc-dropdown-using-selected-label-in-callback-not-value/22003/9) 

#### Output

`my-table` - 

#### Input

`checklist-input-0` - 

`checklist` - 

#### State