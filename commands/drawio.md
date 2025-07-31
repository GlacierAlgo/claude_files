# /drawio Command Specification

## Purpose
The `/drawio` command enables Claude Code to generate professional technical diagrams using Draw.io format, automatically creating visual representations of system architectures, data flows, and component relationships based on code analysis or user specifications.

## Command Syntax
```
/drawio [diagram_type] [source]
```

## Core Behavior
When the `/drawio` command is used, Claude Code should:

1. **Analyze Input**: Parse codebase, requirements, or user description
2. **Extract Components**: Identify systems, services, data flows, and relationships
3. **Generate Structure**: Create logical diagram hierarchy and connections
4. **Apply Styling**: Use consistent visual design patterns
5. **Output XML**: Produce Draw.io compatible XML with embedded styling

## Diagram Types

### System Architecture (`architecture`)
- **Purpose**: High-level system overview showing major components and interactions
- **Elements**: Services, databases, external APIs, data flows
- **Layout**: Layered approach (UI → Logic → Data → Infrastructure)

### Data Flow (`dataflow`) 
- **Purpose**: Visualize data movement and transformation through systems
- **Elements**: Data sources, processing steps, storage, outputs
- **Layout**: Left-to-right flow with clear data transformation points

### Component Relationships (`component`)
- **Purpose**: Detailed view of internal component dependencies and interfaces
- **Elements**: Classes, modules, functions, dependencies
- **Layout**: Hierarchical grouping by domain/responsibility

### API Documentation (`api`)
- **Purpose**: Visual API structure showing endpoints, request/response flows
- **Elements**: Endpoints, request types, data models, authentication
- **Layout**: RESTful resource organization

### Database Schema (`database`)
- **Purpose**: Entity relationships and database structure
- **Elements**: Tables, relationships, indexes, constraints
- **Layout**: Entity-relationship diagram format

## Visual Design Standards

### Color Scheme
- **Infrastructure**: Blue tones (#2196F3, #1976D2)
- **Business Logic**: Green tones (#4CAF50, #388E3C) 
- **Data Storage**: Orange tones (#FF9800, #F57C00)
- **External Services**: Purple tones (#9C27B0, #7B1FA2)
- **User Interface**: Cyan tones (#00BCD4, #0097A7)

### Typography
- **Headers**: Bold, 14pt minimum
- **Labels**: Regular, 10-12pt
- **Details**: Light, 8-10pt
- **Font**: Arial or system default for compatibility

### Layout Principles
- **Consistent Spacing**: 20px minimum between major elements
- **Alignment**: Grid-based positioning for clean appearance
- **Grouping**: Related elements enclosed in containers with subtle backgrounds
- **Flow Direction**: Left-to-right for processes, top-to-bottom for hierarchies

## Implementation Examples

### Basic Usage
```
/drawio architecture src/
```
**Output**: System architecture diagram based on codebase analysis

### Specific Component Analysis
```
/drawio component UserService.py
```
**Output**: Component diagram showing class relationships and dependencies

### Data Flow Visualization
```
/drawio dataflow "user registration process"
```
**Output**: Data flow diagram for user registration workflow

## Generated Output Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="System Architecture" id="generated-id">
    <mxGraphModel dx="1422" dy="794">
      <root>
        <!-- Diagram elements with embedded styling -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Advanced Features

### Auto-Layout Algorithms
- **Force-directed**: For component relationships
- **Hierarchical**: For system architectures
- **Flow-based**: For data and process flows

### Interactive Elements
- **Collapsible Groups**: Hide/show detailed components
- **Hyperlinks**: Link to source code or documentation
- **Tooltips**: Additional context on hover

### Export Options
- **PNG/SVG**: For documentation embedding
- **PDF**: For presentations and reports
- **Draw.io XML**: For further editing

## Integration Points
- **Code Analysis**: Automatic parsing of project structure
- **Documentation**: Generate diagrams for README files
- **Architecture Reviews**: Visual aids for system discussions
- **Onboarding**: Help new developers understand codebase

## Quality Standards
- **Clarity**: All elements clearly labeled and positioned
- **Consistency**: Uniform styling across all diagram types
- **Completeness**: Include all significant components and relationships
- **Accuracy**: Diagrams reflect actual system structure

The `/drawio` command transforms code and system descriptions into professional visual documentation that enhances understanding and communication.
