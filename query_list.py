
query1 = """ #query에 대한 모든 type을 불러오는 query
{
  __schema {
    queryType {
      fields {
        name
      }
    }
  }
}

"""

query2 = """ #query에 대한 정보와 설명을 불러오는 query
{
  __type(name: "Query") {
    name
    description
    fields {
      name
      description
      args {
        name
        description
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
      type {
        name
        kind
        ofType {
          name
          kind
        }
      }
    }
  }
}
"""

query3 = """ #한 시리즈에 대한 정보를 불러오는 query
{
  series(
    id: 2748095
  ) {
    id
    format{
      id
      name
      nameShortened
    }
    private
    startTimeScheduled
    teams{
      baseInfo{
        id
      }
      scoreAdvantage
    }
    title{
      id
      name
    }
    tournament{
      id
      name
      teams{
        id
        name
      }
    }
    type
  }
}
"""

query4 = """ #team의 id 정보를 얻기 위한 query
{
  teams (
    first: 10
  ) {
      totalCount
      pageInfo {
        hasPreviousPage
        hasNextPage
        startCursor
        endCursor
      }
      edges {
        node {
          id
        }
      }
  }
}
"""

query5 = """ #시리즈들의의 정보 추출을 위한 query
{ 
  allSeries(
    first: 50
    filter:{
      titleId: 2
      types: ESPORTS
    }
    orderBy: StartTimeScheduled orderDirection: DESC
  ){
    totalCount
    edges {
      node {
        id
        format{
          id
          name
          nameShortened
        }
        private
        startTimeScheduled
        teams{
          baseInfo{
            id
          }
          scoreAdvantage
        }
        title{
          id
          name
        }
        tournament{
          id
          name
          teams{
            id
            name
          }
        }
        type
      }
    }
  }
}
"""

query6 = """ #series의 id를 추출하는 query
query Get_series_id {
  allSeries(
    first: 50
    filter:{
      titleId: 2
      types: ESPORTS
    }
    orderBy: StartTimeScheduled orderDirection: DESC
  ){
    totalCount,
    pageInfo{
      hasPreviousPage
      hasNextPage
      startCursor
      endCursor
    }
    edges {
      node {
        id
      }
    }
  }
}
"""

query7 = """ #series 안의 게임 정보 추출을 위한 query
query Get_game_state($series_id: ID!) {
  seriesState(
    id: $series_id 
  ) {
    teams {
      score
      won
      kills
      deaths
    }
  }
}
"""