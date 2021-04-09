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

## Modals

### Importing

`import-modal`

`open-import` , `close-import`

The supported files you can export is `.csv` and `.xls.`

You ***must*** follow this column format (this means column name is ***case sensitive*** )

The only required cell to input is `Course ID` but it’s recommended to add a status!

Columns `Course Name`, `Credits`, and `Prerequisites` are automatically filled based on the given `Course ID`


| Course ID | Course Name | Credits | Prerequisites | Status  |
| --------- | ----------- | ------- | ------------- | ------- |
| CMPT 103  | --          | --      | --            | PLANNED |

Below is the raw `.csv` file of the example table above.

```
Course ID,Course Name,Credits,Prerequisites,Status
CMPT 101,,,PLANNED,
```


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

## Intro Modal

`intro-modal`

`open-intro`, `close-intro`

There are **3 columns**: *Find Courses*, *My Table*, and *Checklist*

1. **Find Courses**

   Here you can search for a course’s full description quickly.
   You can search by a course id, course name and, even by a course’s description. As you search, results will update live.

   ![](https://i.imgur.com/rtAsbTD.png) 

   You can select multiple courses and set a status for them. You can also remove them from the table.
   You can choose to import a `csv` or `xls` file to put data into your table. ***Check How to Import for more details*** 

   ![](https://i.imgur.com/h6koO6e.png?1)

   In the future, you will be able to switch to a sunburst view, showing the relation of courses in your table more visually. For now we’ll have to stick with the table 😅.

2. **My Table**

   This table represents your Computer Science Major degree plan.
   Every time you make changes from the ***Mark selected courses(s) as:*** section, it will be added to you table.
   You can export your table at any point into a `.csv` fille.

   Within the table, you can filter the data. You can filter by string or number, depending on the column.

   ![](https://i.imgur.com/Q9g4VFR.png) 

   The official docs on filtering tables can be found [here](https://bit.ly/31tUrjG).

   **Text & String Filtering**

   - `United`
   - `= United`
   - `United States`
   - `"United States"`
   - `= United States`
   - `= "United States"`
   - `> United`
   - `>= United`
   - `< United`	
   - `<= United`

   **Numeric Filtering**

   - `43.828`
   - `= 43.828`
   - `> 43.828`
   - `>= 43.828`
   - `< 43.828`
   - `<= 43.828`

   Below the table, are where you can go back to this window if you ever get lost. You can also find helpful information here like ***How to Import***.

3. **Checklist**

   Finally, the checklist. The dropdown allows you to change your checklist requirements based on the stream you choose.

   The default stream is the *Gaming Stream*.

   ![](https://i.imgur.com/rXgKu7e.png) 

   In the future, any updates to your table will be able to reflect on you checklist.

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